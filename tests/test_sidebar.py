import pytest

from components.sidebar import _get_api_key_from_secrets


SECRETS_TOML = """\
[openai]
api_key = "sk-openai-secret"

[anthropic]
api_key = "sk-anthropic-secret"
"""


def _patch_sidebar_project_root(monkeypatch, project_root):
    """Make components.sidebar resolve its project root to *project_root*."""
    fake_sidebar_file = project_root / "components" / "sidebar.py"
    fake_sidebar_file.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("components.sidebar.__file__", str(fake_sidebar_file))


def test_get_api_key_from_secrets_loads_from_project_root(tmp_path, monkeypatch):
    """API keys should be read from the project-root secrets.toml regardless of cwd."""
    project_root = tmp_path / "repo"
    project_root.mkdir()
    secrets_file = project_root / ".streamlit" / "secrets.toml"
    secrets_file.parent.mkdir(parents=True)
    secrets_file.write_text(SECRETS_TOML)

    _patch_sidebar_project_root(monkeypatch, project_root)

    # Run from a completely different working directory
    other_dir = tmp_path / "elsewhere"
    other_dir.mkdir()
    monkeypatch.chdir(other_dir)

    assert _get_api_key_from_secrets("OpenAI") == "sk-openai-secret"
    assert _get_api_key_from_secrets("Anthropic") == "sk-anthropic-secret"


def test_get_api_key_from_secrets_returns_empty_when_missing(tmp_path, monkeypatch):
    """Should return an empty string when no local secrets.toml exists."""
    project_root = tmp_path / "repo"
    project_root.mkdir()

    _patch_sidebar_project_root(monkeypatch, project_root)

    other_dir = tmp_path / "elsewhere"
    other_dir.mkdir()
    monkeypatch.chdir(other_dir)

    assert _get_api_key_from_secrets("OpenAI") == ""


def test_get_api_key_from_secrets_swallows_streamlit_secret_error(
    tmp_path, monkeypatch
):
    """A missing/invalid secrets configuration must never crash the app."""
    project_root = tmp_path / "repo"
    project_root.mkdir()

    _patch_sidebar_project_root(monkeypatch, project_root)

    # Force st.secrets to raise the exact error the user reported
    def raising_get(*args, **kwargs):
        from streamlit.errors import StreamlitSecretNotFoundError

        raise StreamlitSecretNotFoundError("No secrets found")

    monkeypatch.setattr("streamlit.runtime.secrets.Secrets.__getitem__", raising_get)
    monkeypatch.setattr("streamlit.runtime.secrets.Secrets.get", raising_get)

    assert _get_api_key_from_secrets("OpenAI") == ""


def test_get_api_key_from_secrets_falls_back_to_st_secrets(tmp_path, monkeypatch):
    """When no local secrets.toml exists, st.secrets (e.g. Streamlit Cloud) is used."""
    project_root = tmp_path / "repo"
    project_root.mkdir()

    _patch_sidebar_project_root(monkeypatch, project_root)

    class FakeSecrets:
        def get(self, key, default=None):
            return {"openai": {"api_key": "sk-cloud"}}.get(key, default)

    monkeypatch.setattr("components.sidebar.st.secrets", FakeSecrets())

    assert _get_api_key_from_secrets("OpenAI") == "sk-cloud"
