---
tags: [author-review]
---
# Author review

Author notes whose **verified** box is still unchecked. Open one, check the person, photo, bio and current affiliation against their own page, then tick `verified` in its properties and it drops off this list.

```dataview
TABLE WITHOUT ID length(rows) AS "Still to verify"
FROM #author
WHERE !verified
GROUP BY true
```

```dataview
TABLE affiliation AS "Affiliation", affiliation-checked AS "Checked", wikidata AS "Wikidata"
FROM #author
WHERE !verified
SORT file.name ASC
```

## Verified

```dataview
LIST
FROM #author
WHERE verified
SORT file.name ASC
```
