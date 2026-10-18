import app.memory as memory


def test_memory_is_scoped_to_user(tmp_path, monkeypatch):
    monkeypatch.setattr(memory, "DB_PATH", tmp_path / "test-memory.db")

    memory.save_memory("user-a", "Prefers concise answers")
    memory.save_memory("user-b", "Prefers detailed answers")

    assert memory.get_memories("user-a") == ["Prefers concise answers"]
    assert memory.get_memories("user-b") == ["Prefers detailed answers"]


def test_empty_memory_is_rejected():
    import pytest

    with pytest.raises(ValueError, match="cannot be empty"):
        memory.save_memory("user-a", "  ")
