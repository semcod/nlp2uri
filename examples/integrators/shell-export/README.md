# Shell export integrator

Generates bash `export` lines for reuse in scripts:

```bash
eval "$(nlp2uri shell export 'open firefox' --platform linux)"
echo "$NLP2URI_URI"
$nlp2uri-run   # alias to compiled command
```

Raw URI:

```bash
eval "$(nlp2uri shell eval-uri 'app://firefox/open' --platform linux)"
```

## Run

```bash
./e2e.sh
```
