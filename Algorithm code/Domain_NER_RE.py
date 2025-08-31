git clone https://github.com/nlpaueb/finer

# Domain-Specific Named Entity Recognizer using Regular Expressions
# Financial News Example

import re
import pandas as pd

# 1. Define Regex Patterns
# Financial Figures: $1.2B, €500M, ¥1.2 trillion, 4 million dollars, etc.
financial_figure_patterns = [
    r'\$\s?\d+[\.,]?\d*\s?[MBTK]?',                     # $1.2B, $500M
    r'€\s?\d+[\.,]?\d*\s?[MBTK]?',                      # €500M
    r'¥\s?\d+[\.,]?\d*\s?(million|billion|trillion)?',  # ¥1.2 trillion
    r'\d+[\.,]?\d*\s?(million|billion|trillion)?\s?(dollars|euros|yen)',  # 4 million dollars
]

# Stock Movements: +5.6%, -$0.75, etc.
stock_movement_patterns = [
    r'[\+\-]\d+(\.\d+)?\s?%',      # +5.6%, -4%
    r'[\+\-]\$\d+(\.\d+)?',        # +$0.75, -$1.50
]

# Financial Quarters: Q4 2024, Q1 2023, etc.
quarter_patterns = [
    r'Q[1-4]\s*\d{4}',
]

# Company Names - simple heuristic: Capitalized word sequences, or "Inc.", "Ltd.", "Corp.", etc.
company_patterns = [
    r'([A-Z][a-zA-Z0-9&.,\- ]+(Inc\.|Ltd\.|Corp\.|LLC|PLC))',
    r'([A-Z][a-zA-Z0-9&.,\- ]{2,})'
]

# Contextual Keywords for Figures
keywords = ['revenue', 'net profit', 'earnings', 'income', 'loss', 'growth', 'decline']

# 2. Function to Extract Entities from Text
def extract_entities(article_text):
    results = {
        'Article_Title': '',
        'Company_Name': [],
        'Mentioned_Revenue': [],
        'Stock_Change': [],
        'Quarter': [],
    }

    # TITLE (assume first line or given separately)
    title_match = re.findall(r'^[^\n]+', article_text)
    if title_match:
        results['Article_Title'] = title_match[0].strip()
    else:
        results['Article_Title'] = ''

    # Find Company Names
    companies = set()
    for patt in company_patterns:
        found = re.findall(patt, article_text)
        for res in found:
            cname = res[0] if isinstance(res, tuple) else res
            companies.add(cname.strip())
    results['Company_Name'] = list(companies) if companies else ['Unknown']

    # Find Mentioned Revenues and Context
    for fg_pat in financial_figure_patterns:
        for match in re.finditer(fg_pat, article_text):
            # Check for nearby keywords
            left_window = article_text[max(0, match.start()-40):match.start()]
            if any(kw in left_window.lower() for kw in keywords):
                results['Mentioned_Revenue'].append(match.group().strip())

    # Stock movements
    for sm_pat in stock_movement_patterns:
        for match in re.finditer(sm_pat, article_text):
            results['Stock_Change'].append(match.group().strip())

    # Quarters
    for q_pat in quarter_patterns:
        for match in re.finditer(q_pat, article_text):
            results['Quarter'].append(match.group().strip())

    return results

# 3. Function to Process Multiple Articles and Save to CSV
def process_articles(filelist, output_csv='financial_entities.csv'):
    all_results = []
    for filename in filelist:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            entities = extract_entities(text)
            # Flatten lists for CSV
            entities['Company_Name'] = ', '.join(set(entities['Company_Name']))
            entities['Mentioned_Revenue'] = ', '.join(set(entities['Mentioned_Revenue']))
            entities['Stock_Change'] = ', '.join(set(entities['Stock_Change']))
            entities['Quarter'] = ', '.join(set(entities['Quarter']))
            all_results.append(entities)

    df = pd.DataFrame(all_results)
    df.to_csv(output_csv, index=False)
    print(f'Saved to {output_csv}')
    return df

# 4. Example Usage in Colab
# You can replace 'sample_financial_news.txt' with your own uploaded files
'''
file_list = ['sample_financial_news1.txt', 'sample_financial_news2.txt']
df = process_articles(file_list)
print(df)
'''

# 5. For Quick Testing, Use Inline Strings
if __name__ == "__main__":
    article = """
    Acme Corp. Reports Record Revenue of $1.2B in Q2 2024. Net profit surged +5.6% compared to last year.
    The company's earnings rose to €800M, while net income was ¥1.2 trillion. After the announcement,
    Acme Corp.'s stock price jumped +$0.75. Beta-Global Inc. posted a revenue of 4 million dollars in Q1 2023.
    """

    entities = extract_entities(article)
    print(pd.DataFrame([{
        'Article_Title': entities['Article_Title'],
        'Company_Name': ', '.join(entities['Company_Name']),
        'Mentioned_Revenue': ', '.join(entities['Mentioned_Revenue']),
        'Stock_Change': ', '.join(entities['Stock_Change']),
        'Quarter': ', '.join(entities['Quarter']),
    }]))

