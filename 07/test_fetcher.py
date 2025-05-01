from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from fetcher import URLFetcher, load_urls


@pytest.mark.asyncio
async def test_get_top_words():
    fetcher = URLFetcher(concurrency=2)
    text = "Hello world! Hello everyone. Hello again, world world."
    top_words = fetcher.get_top_words(text, top_n=2)
    assert top_words == [('hello', 3), ('world', 3)]


def test_load_urls(tmp_path):
    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("http://example.com\nhttps://test.com\n")
    urls = load_urls(str(urls_file))
    assert urls == ["http://example.com", "https://test.com"]


@pytest.mark.asyncio
async def test_fetch_success():
    fetcher = URLFetcher(concurrency=1)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.text = AsyncMock(return_value="test page content test")

    mock_session = MagicMock()
    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_response
    mock_session.get.return_value = mock_context_manager

    url = "http://example.com"
    fetched_url, status, top_words = await fetcher.fetch(mock_session, url)

    assert fetched_url == url
    assert status == 200
    assert top_words[0][0] == "test"


@pytest.mark.asyncio
async def test_fetch_failure():
    fetcher = URLFetcher(concurrency=1)

    mock_session = AsyncMock()
    mock_session.get.side_effect = Exception("Connection failed")

    url = "http://invalid-url.com"
    fetched_url, status, top_words = await fetcher.fetch(mock_session, url)

    assert fetched_url == url
    assert status is None
    assert top_words == []


@pytest.mark.asyncio
async def test_run_multiple_fetches():
    fetcher = URLFetcher(concurrency=2)

    urls = ["http://example1.com", "http://example2.com"]

    with patch.object(fetcher, 'fetch', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = ("http://example.com", 200, [('example', 5)])

        results = await fetcher.run(urls)

        assert len(results) == 2
        for result in results:
            assert result[1] == 200
            assert result[2][0][0] == 'example'
