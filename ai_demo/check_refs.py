"""Check whether each AI-generated reference exists (Crossref + PubMed).

Run:  python -I check_refs.py
Writes ref_check.csv next to this file. Checks existence and bibliographic
match only (title, year, volume, first page). It does NOT judge whether the
paper supports the sentence it was cited for; that is done by reading.
"""
import csv, json, re, time, urllib.parse, urllib.request
from difflib import SequenceMatcher
from pathlib import Path

REFS = [
    # key, first author, title, year, volume, first page, journal
    ("FloresMireles2015", "Flores-Mireles", "Urinary tract infections: epidemiology, mechanisms of infection and treatment options", 2015, "13", "269", "Nat Rev Microbiol"),
    ("Murray2022", "Murray", "Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis", 2022, "399", "629", "Lancet"),
    ("Pitout2008", "Pitout", "Extended-spectrum beta-lactamase-producing Enterobacteriaceae: an emerging public-health concern", 2008, "8", "159", "Lancet Infect Dis"),
    ("Bush2010", "Bush", "Updated functional classification of beta-lactamases", 2010, "54", "969", "Antimicrob Agents Chemother"),
    ("Gupta2011", "Gupta", "International clinical practice guidelines for the treatment of acute uncomplicated cystitis and pyelonephritis in women: a 2010 update by the Infectious Diseases Society of America and the European Society for Microbiology and Infectious Diseases", 2011, "52", "e103", "Clin Infect Dis"),
    ("Woerther2013", "Woerther", "Trends in human fecal carriage of extended-spectrum beta-lactamases in the community: toward the globalization of CTX-M", 2013, "26", "744", "Clin Microbiol Rev"),
    ("Laxminarayan2016a", "Laxminarayan", "Access to effective antimicrobials: a worldwide challenge", 2016, "387", "168", "Lancet"),
    ("Kumarasamy2010", "Kumarasamy", "Emergence of a new antibiotic resistance mechanism in India, Pakistan, and the UK: a molecular, biological, and epidemiological study", 2010, "10", "597", "Lancet Infect Dis"),
    ("Rawat2010", "Rawat", "Extended-spectrum beta-lactamases in Gram negative bacteria", 2010, "2", "263", "J Glob Infect Dis"),
    ("Paterson2005", "Paterson", "Extended-spectrum beta-lactamases: a clinical update", 2005, "18", "657", "Clin Microbiol Rev"),
    ("Laxminarayan2013", "Laxminarayan", "Antibiotic resistance - the need for global solutions", 2013, "13", "1057", "Lancet Infect Dis"),
    ("Laxminarayan2016b", "Laxminarayan", "Antibiotic resistance in India: drivers and opportunities for action", 2016, "13", "e1001974", "PLoS Med"),
    ("Walia2019", "Walia", "Establishing antimicrobial resistance surveillance & research network in India: journey so far", 2019, "149", "164", "Indian J Med Res"),
    ("ICMR_AMRSN_2022", "ICMR", "Antimicrobial Resistance Research and Surveillance Network: Annual Report, January 2022 to December 2022", 2023, "", "", "ICMR report (grey literature)"),
]

UA = {"User-Agent": "teaching-deck-ref-check/1.0"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def norm(s):
    s = (s or "").lower().replace("β", "beta")
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def sim(a, b):
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def crossref(author, title):
    q = urllib.parse.urlencode({"query.bibliographic": f"{title} {author}", "rows": 3})
    items = get("https://api.crossref.org/works?" + q)["message"]["items"]
    best = None
    for it in items:
        t = (it.get("title") or [""])[0]
        s = sim(t, title)
        if best is None or s > best[0]:
            yr = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
            cont = " ".join(it.get("container-title") or []) + " " + " ".join(it.get("short-container-title") or [])
            best = (s, t, it.get("DOI", ""), yr, it.get("volume", ""), it.get("page", "") or it.get("article-number", ""), cont)
    return best


def pubmed(title, journal="", vol="", page="", year=""):
    """Find PMIDs by journal+volume+first page, then confirm the title with esummary."""
    if not (journal and vol and page):
        return []
    found = _by_citation(title, journal, vol, page)
    if found:
        return found
    # fallback: title search, accept only close title matches
    term = urllib.parse.quote(" ".join(title.split()[:12]) + "[Title]")
    ids = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term={term}")["esearchresult"].get("idlist", [])
    if not ids:
        return []
    summ = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=" + ",".join(ids))["result"]
    return [i for i in ids if sim(summ[i].get("title", ""), title) >= 0.8 and str(year) in summ[i].get("pubdate", "")]


def _by_citation(title, journal, vol, page):
    pg = re.sub(r"^e", "e", page)
    term = urllib.parse.quote(f'"{journal}"[Journal] AND {vol}[Volume] AND {pg}[Page]')
    ids = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term={term}")["esearchresult"].get("idlist", [])
    if not ids:
        return []
    summ = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=" + ",".join(ids))["result"]
    return [i for i in ids if sim(summ[i].get("title", ""), title) >= 0.8]


rows = []
for key, author, title, year, vol, page, journal in REFS:
    cr = pm = None
    try:
        cr = crossref(author, title)
    except Exception as e:  # keep going; record the error
        cr = ("ERR", str(e), "", "", "", "", "")
    time.sleep(0.4)
    try:
        pm = pubmed(title, journal, vol, page, year) if "grey" not in journal else []
    except Exception as e:
        pm = ["ERR:" + str(e)]
    time.sleep(0.4)
    s, t, doi, cyr, cvol, cpage, cont = cr
    # accept a Crossref hit only if title AND journal match (Crossref often returns look-alike items)
    ok_title = isinstance(s, float) and s >= 0.85 and sim(cont, journal) >= 0.35 or (isinstance(s, float) and s >= 0.85 and norm(journal).split()[0] in norm(cont))
    if not ok_title:
        t = doi = cyr = cvol = cpage = ""  # weak Crossref match: do not record a wrong DOI
    rows.append({
        "key": key, "journal_as_cited": journal, "year_as_cited": year,
        "volume_as_cited": vol, "first_page_as_cited": page,
        "crossref_title_similarity": round(s, 2) if isinstance(s, float) else s,
        "crossref_title": t, "doi": doi, "crossref_year": cyr,
        "crossref_volume": cvol, "crossref_pages": cpage,
        "year_match": str(cyr) == str(year) if ok_title else "",
        "volume_match": (cvol == vol) if ok_title and vol else "",
        "first_page_match": str(cpage).split("-")[0] == page if ok_title and page else "",
        "pubmed_ids": ";".join(pm),
        "exists_title_match": "yes" if (ok_title or pm) and "grey" not in journal else "not checked (grey literature)" if "grey" in journal else "NO MATCH",
    })
    print(key, rows[-1]["exists_title_match"], rows[-1]["crossref_title_similarity"], rows[-1]["doi"])

out = Path(__file__).with_name("ref_check.csv")
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print("wrote", out)
