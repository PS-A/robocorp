from robocorp import workitems
from robocorp.tasks import task
from RPA.PDF import PDF
from pathlib import Path

# Paths and folders.
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

@task
def consume_news_data():
    """Go over the workitems and create News Digest PDFs."""
    pdf = PDF()

    for item in workitems.inputs:
        try:
            payload = item.payload if isinstance(item.payload, dict) else {}
            html = generate_html(payload)
            pdf_path = OUTPUT/f"News_digest_{payload.get('keyword')}_from_{payload.get('from_date')}.pdf"
            pdf.html_to_pdf(html, str(pdf_path))

            item.done()
            print(f"Created news digest {pdf_path}.")
        except Exception as e:
            item.fail(f"Failed to create news digest: {e}.")
            print(f"Error: {e}")

def generate_html(payload):
    html_parts = []

    # Cover page.
    html_parts.append(f"""
                    <html><head>
                    <meta charset="utf-8">
                    </head><body>
                    <h1>News Digest</h1>
                    <p><b>Keyword:</b> {payload.get('keyword')}<br>
                    <b>From date:</b> {payload.get('from_date')}<br>
                    <b>Sorted by:</b> {payload.get('sort_by')}<br>
                    <b>Fetched time:</b> {payload.get('fetched_time')}<br>
                    <b>Total results:</b> {payload.get('total_results')}</p>
                    <br><br>
                    """)
    
    # Article pages.
    for a in payload.get('articles'):
        src = a.get('source').get('name')
        author = a.get('author') or ''
        published = a.get('publishedAt') or ''
        meta = " · ".join([x for x in (src, author, published) if x])

        html_parts.append(f"""
                        <h2>{a.get('title')}</h2>
                        <p><i>{meta}</i></p>
                        <p>{a.get('description')}</p>
                        <p><a href="{a.get('url')}">{a.get('url')}</a></p>
                        <br><br>
                        """)
        
    html_parts.append("</body></html>")
    return "".join(html_parts)