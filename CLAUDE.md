# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリの性質

wingconsulting.org の公開サイト。**ビルド工程を持たない静的 HTML の集合**で、Netlify が
`publish = "."` でそのまま配信する。`package.json` もテストもリンタも無い。
編集した HTML がそのまま本番の HTML になるので、書いた内容が即公開物になる前提で扱う。

このリポジトリは **GitHub で公開されている**。合言葉・キー・顧客名など、
出せない値は一切置かない（`netlify/edge-functions/staypath-gate.ts` の冒頭コメントに経緯がある）。

## 構成

| 場所 | 中身 |
|---|---|
| ルート直下 | `index` / `about` / `privacy` / `dx-assessment` と製品ページ `*-guide.html` |
| `blog/` | 記事39本 + `index.html`（カテゴリ別索引） |
| `staypath/` | 別リポジトリでビルドした SPA の成果物（後述） |
| `netlify/edge-functions/` | StayPath の入口認証 |
| `images/og/` | 記事ごとの OG 画像。1200x630、ファイル名は記事スラッグと一致 |

`_faqs.json` / `_svcs.json` はどの HTML からも参照されていない。触る前に用途を確かめること。

## デプロイ

Netlify。`main` への push で公開される。ビルドコマンドは無い。
ヘッダー・リダイレクト・Edge Function の割り当ては `netlify.toml` に集約されている。

## StayPath（/staypath/）

外国人材受入支援の業務管理システム。**本体のソースはこのリポジトリに無い**。
ここに置いてあるのはビルド成果物（`staypath/assets/*.js`）だけなので、
アプリの挙動を直す依頼はこのリポジトリでは扱えない。

本体の在り処（**こちらで作業する**）:

    ~/dev/staypath

React 19 + Vite + TypeScript。Supabase / docx / xlsx / jszip を使う。
公開用の成果物は **`npm run build:deploy`** で作り、出力（`dist/`）を
このリポジトリの `staypath/` へ配置する。

    cd ~/dev/staypath && npm run build:deploy
    rm -f ~/dev/wingconsulting_Web/staypath/assets/*
    cp -r dist/assets/* ~/dev/wingconsulting_Web/staypath/assets/
    cp dist/index.html ~/dev/wingconsulting_Web/staypath/index.html

素の `npm run build` を使わないこと。`vite.config.ts` の base が
`DEPLOY_BASE ?? '/'` なので、渡さないと `index.html` が `/assets/…` を指す。
そのパスにファイルは無く、SPA の受け皿が `index.html` を返すため、
JS と CSS として読めずに**画面が真っ白になる**（2026-09-01 に実際に起きた）。
配置したら `staypath/index.html` の参照先が `/staypath/assets/…` かを必ず目視する。

ビルドには `.env`（`VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY`）が要る。
無いまま作ると接続先が空の成果物ができる。値は公開済みバンドルにも入っている公開鍵。

`~/Desktop/GoogleDrive-…/staypath/` にも同じ履歴の複製がある（元はこちらだけだった）。
Google Drive 配下で同期事故が起きやすいので、**編集は `~/dev/staypath` 側で行う**。
両方に作業コピーがあるため、片方だけ直すと食い違う点に注意。

- バックエンドは Supabase（プロジェクト `wpocesolyipjnfnkmhwi`）。データは行レベル権限で保護
- SPA のため `netlify.toml` のリダイレクトで、実ファイルが無ければ `index.html` を返す
- 入口に Basic 認証。合言葉は Netlify 環境変数 `STAYPATH_USER` / `STAYPATH_PASS`
- 受付フォーム（`/staypath/form/`, `/staypath/liff/`）は `?t=` 付きのときだけ門を通す。
  応募者・企業・送り出し機関は LINE から届いた URL を開くだけの相手で、合言葉を渡せないため
- 面談の録音にマイクを使うので、この配下だけ `Permissions-Policy` で microphone を許可している
- 検索避けは `X-Robots-Tag: noindex`。**robots.txt では弾かない**（理由は robots.txt のコメント参照）

## ページを足す・直すときに一緒に触るもの

記事やページを1本足すと以下がセットで必要になる。片方だけ直すと食い違う。

1. `sitemap.xml` … `<loc>` と `<lastmod>`
2. `llms.txt` … AI 検索向けの索引。主要記事は1行要約を添える
3. `blog/index.html` … 記事一覧のカード
4. `images/og/<スラッグ>.png` … 1200x630
5. 記事内の JSON-LD … `Article` / `BreadcrumbList` / `WebPage`。
   `datePublished` と `dateModified` は **JSON-LD と本文の双方**に書く

## SEO / GEO の方針

- AI 検索クローラー（GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended）を
  robots.txt で明示的に Allow している
- 全ページ静的 HTML。本文を JS で生成しない
- GA4 は `G-KN7NWHFK9G`。`<head>` の先頭に gtag を置く（Google の所有権確認ファイルを除く全 HTML に入っている）
- canonical は `https://wingconsulting.org/<パス>`（拡張子なし）

## コミットメッセージ

日本語で書く。既存のログに合わせること。

- **件名** … StayPath の変更は `StayPath: 〜`、サイト側はそのまま用件を書く。
  `feat:` のような英語の prefix は使わない
- **本文** … 何を直したかより「**なぜそうなっていたか / 直さないと何が起きるか**」を書く。
  節は `■ 見出し` で区切る
- 実データの件数を根拠として添える（例:「117件中117件が空」「紐づけは332社中2件」）
- 「機械が推測して勝手に決める挙動は作らない」という判断が繰り返し出てくる。同じ基準で書く

## 書き言葉

サイト本文・コード内コメント・コミットのすべてで**平易な日本語**を使う。
カタカナの専門用語を並べず、「合言葉」「置き場」「門」のように普通の言葉に置き換える。
`netlify.toml` / `robots.txt` / `staypath-gate.ts` のコメントが見本。
