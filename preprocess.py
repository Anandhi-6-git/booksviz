diff --git a//dev/null b/preprocess.py
index 0000000000000000000000000000000000000000..c3046b58bf54333174eb85777a7121e055b07020 100644
--- a//dev/null
+++ b/preprocess.py
@@ -0,0 +1,44 @@
+import pandas as pd
+import json
+import os
+import argparse
+
+parser = argparse.ArgumentParser(description='Preprocess Goodreads data')
+parser.add_argument('--input', default='GoodReads_100k_books.csv.xz', help='Input CSV file')
+parser.add_argument('--output', default='scatter_data.json', help='Output JSON file')
+parser.add_argument('--sample', type=int, default=5000, help='Max sample size')
+args = parser.parse_args()
+
+# Load
+print('Reading', args.input)
+df = pd.read_csv(args.input, low_memory=False)
+
+# Select and compute columns
+cols = ['pages', 'desc', 'reviews', 'rating']
+df = df[cols]
+df['blurb'] = df['desc'].fillna('').astype(str).str.len()
+df = df.drop(columns='desc')
+
+# Ensure numeric
+for c in ['pages', 'reviews', 'rating', 'blurb']:
+    df[c] = pd.to_numeric(df[c], errors='coerce')
+
+# Outlier clipping
+mask = pd.Series(True, index=df.index)
+for c in ['pages', 'blurb', 'reviews', 'rating']:
+    low = df[c].quantile(0.005)
+    high = df[c].quantile(0.995)
+    mask &= df[c].between(low, high)
+df = df[mask]
+
+# Sample
+if len(df) > args.sample:
+    df = df.sample(n=args.sample, random_state=42)
+
+# Save JSON
+records = df.to_dict(orient='records')
+with open(args.output, 'w') as f:
+    json.dump(records, f, separators=(',', ':'))
+
+size = os.path.getsize(args.output)
+print('Wrote', args.output, 'size:', size, 'bytes')
diff --git a//dev/null b/preprocess.py
index 0000000000000000000000000000000000000000..c3046b58bf54333174eb85777a7121e055b07020 100644
--- a//dev/null
+++ b/preprocess.py
@@ -0,0 +1,44 @@
+import pandas as pd
+import json
+import os
+import argparse
+
+parser = argparse.ArgumentParser(description='Preprocess Goodreads data')
+parser.add_argument('--input', default='GoodReads_100k_books.csv.xz', help='Input CSV file')
+parser.add_argument('--output', default='scatter_data.json', help='Output JSON file')
+parser.add_argument('--sample', type=int, default=5000, help='Max sample size')
+args = parser.parse_args()
+
+# Load
+print('Reading', args.input)
+df = pd.read_csv(args.input, low_memory=False)
+
+# Select and compute columns
+cols = ['pages', 'desc', 'reviews', 'rating']
+df = df[cols]
+df['blurb'] = df['desc'].fillna('').astype(str).str.len()
+df = df.drop(columns='desc')
+
+# Ensure numeric
+for c in ['pages', 'reviews', 'rating', 'blurb']:
+    df[c] = pd.to_numeric(df[c], errors='coerce')
+
+# Outlier clipping
+mask = pd.Series(True, index=df.index)
+for c in ['pages', 'blurb', 'reviews', 'rating']:
+    low = df[c].quantile(0.005)
+    high = df[c].quantile(0.995)
+    mask &= df[c].between(low, high)
+df = df[mask]
+
+# Sample
+if len(df) > args.sample:
+    df = df.sample(n=args.sample, random_state=42)
+
+# Save JSON
+records = df.to_dict(orient='records')
+with open(args.output, 'w') as f:
+    json.dump(records, f, separators=(',', ':'))
+
+size = os.path.getsize(args.output)
+print('Wrote', args.output, 'size:', size, 'bytes')

