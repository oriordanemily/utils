import pytest
import pandas as pd
from utils.python.display import add_caption_to_df

@pytest.fixture
def sample_df():
    """Creates a simple DataFrame for testing."""
    return pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

def test_add_caption_to_df(sample_df):
    """Tests if the function correctly applies a caption and styles."""
    caption_text = "Test Caption"
    styled_df = add_caption_to_df(sample_df, caption_text)

    # Check if returned object is a Styler
    assert isinstance(styled_df, pd.io.formats.style.Styler), "Function did not return a Styler object"

    # Check if caption is correctly set
    assert styled_df.caption == caption_text, "Caption was not correctly applied"

    # Check if styles include the expected caption styling
    styles = styled_df.table_styles
    found_caption_style = any(
        style['selector'] == 'caption' and 
        ('text-align', 'center') in style['props'] and 
        ('color', 'black') in style['props'] 
        for style in styles
    )

    assert found_caption_style, "Caption styles were not correctly applied"

def test_add_caption_custom_color(sample_df):
    """Tests if a custom color is applied correctly."""
    styled_df = add_caption_to_df(sample_df, "Custom Caption", color="red")

    # Check if the custom color is applied
    styles = styled_df.table_styles
    found_color_style = any(
        style['selector'] == 'caption' and 
        ('color', 'red') in style['props'] 
        for style in styles
    )

    assert found_color_style, "Custom color was not applied correctly"

def test_add_caption_invalid_df():
    """Tests that passing an invalid dataframe raises an error."""
    with pytest.raises(AttributeError):
        add_caption_to_df(None, "Invalid Test")  # Should fail because None is not a DataFrame
