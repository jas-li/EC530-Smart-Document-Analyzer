import sys
# Append the path to the directory containing the module
sys.path.append('../flask-app')
import pytest
from unittest.mock import patch, MagicMock
import feed_ingest
from PIL import Image
from bson import ObjectId

# Mock configurations and external dependencies
@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('feed_ingest.PyPDF2.PdfReader') as mock_pdf_reader:
        with patch('feed_ingest.pytesseract.image_to_string') as mock_tesseract:
            with patch('feed_ingest.get_files') as mock_get_files:
                with patch('feed_ingest.gridfs.GridFS.get') as mock_gridfs_get:
                    with patch('feed_ingest.Article') as mock_article:
                        # Set up mocks
                        mock_pdf_reader.return_value.pages = [MagicMock(extract_text=lambda: "Sample text")]
                        mock_tesseract.return_value = "Extracted image text"
                        mock_get_files.return_value = ({"sample.pdf": "12345"}, 200)
                        mock_gridfs_get.return_value = MagicMock(read=lambda: b"PDF data")
                        mock_article_instance = mock_article.return_value
                        mock_article_instance.download.return_value = None
                        mock_article_instance.parse.return_value = None
                        mock_article_instance.text = "Article text"
                        mock_article_instance.title = "Test Article"
                        mock_article_instance.authors = ["Author One"]
                        mock_article_instance.publish_date = "2021-01-01"
                        mock_article_instance.top_image = "http://example.com/image.jpg"
                        mock_article_instance.keywords = ["news", "test"]
                        mock_article_instance.summary = "Summary of the article"

                        yield

def test_pdf_to_text():
    assert feed_ingest.pdf_to_text("path/to/sample.pdf") == "Sample text"

def test_image_to_text():
    with patch('feed_ingest.Image.open', return_value=MagicMock(spec=Image.Image)):
        assert feed_ingest.image_to_text("path/to/sample.jpg") == "Extracted image text"

# def test_convert_file_success_pdf():
#     result, status = feed_ingest.convert_file("RN100_Extra_Credit.pdf", ObjectId("663566e8a0a5e2f51858a729"))
#     assert status == 200
#     assert result == "Sample text"

def test_convert_file_not_found():
    with patch('feed_ingest.get_files', return_value=({}, 404)):
        result, status = feed_ingest.convert_file("missing.pdf", ObjectId("663566e8a0a5e2f51858a729"))
        assert status == 500
        assert result == "Error: Unable to retrieve files"

def test_extract_web_content():
    result = feed_ingest.extract_web_content("http://valid.url")
    assert result['title'] == "Test Article"
    assert result['text'] == "Article text"

# More tests can be added to cover other edge cases and error handling scenarios
