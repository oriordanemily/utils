import pandas as pd

def add_caption_to_df(df, caption, color='black', fontsize=100):
    """Mainly to be used for display in Jupyter notebooks."""
    styles = [dict(selector="caption",
                       props=[("text-align", "center"),
                              ("font-size", "100%"),
                              ("color", color)])]

    df = df.style.set_caption(caption).set_table_styles(styles)

    return df