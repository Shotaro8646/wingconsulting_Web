import type { Context } from 'https://edge.netlify.com'

/**
 * StayPath の入口。合言葉を知らない相手には画面そのものを出さない。
 *
 * 中のデータは Supabase の行レベル権限で守られていて、
 * ログインしない限り1件も読めないことは実際に叩いて確かめてある。
 * ただし「ログイン画面が誰にでも見えている」状態ではあった。
 *
 * URL を推測されにくいものに変える案は使えない。
 * このサイトの配信元リポジトリが GitHub で公開されており、
 * パスがファイル一覧に出てしまう。同じ理由で合言葉も git に置けない。
 * 残るのは HTTP の入口で止める方法だけなので、ここで Basic 認証を掛ける。
 *
 * 受付フォームだけは通す。応募者・企業・送り出し機関は
 * LINE から届いた URL を開くだけの相手で、合言葉を渡せないため。
 * ただし合言葉つきの URL（?t=）でないと通さない。
 * 素の /staypath/form/company を打っただけでは開かない。
 */

/** 合言葉が無くても通す道。どれも「リンクを渡した相手」しか来ない */
function isOpen(url: URL): boolean {
  const p = url.pathname

  // 画面を動かす部品。フォームが読み込むので閉じられない。
  // これ単体を取っても、中の入れ物（index.html）が無ければ何も動かない
  if (p.startsWith('/staypath/assets/')) return true

  // LINE がリッチメニューの画像を取りに来る。認証は付けられない
  if (p === '/staypath/richmenu.png' || p === '/staypath/richmenu.html') return true

  // 受付フォーム。合言葉つきの URL のときだけ通す。
  // 合言葉そのものの正しさは、この先の画面と行レベル権限が確かめる
  if (p.startsWith('/staypath/form/') || p.startsWith('/staypath/liff/')) {
    return !!url.searchParams.get('t')
  }

  return false
}

/** 一致の判定で、長さの違いから当たりを絞られないようにする */
function same(a: string, b: string): boolean {
  if (a.length !== b.length) return false
  let diff = 0
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i)
  return diff === 0
}

const ASK = {
  'WWW-Authenticate': 'Basic realm="StayPath", charset="UTF-8"',
  'Content-Type': 'text/html; charset=utf-8',
  'Cache-Control': 'no-store',
  'X-Robots-Tag': 'noindex, nofollow',
}

const page = (title: string, body: string) => `<!doctype html>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title}</title>
<style>
 body{margin:0;min-height:100vh;display:grid;place-items:center;background:#F8F7F4;
  font-family:"Meiryo","メイリオ",sans-serif;color:#14181F;line-height:1.8}
 main{max-width:29rem;padding:2rem}
 h1{font-size:1.05rem;font-weight:700;margin:0 0 .75rem}
 p{font-size:.85rem;color:#4A515C;margin:0 0 .6rem}
 code{background:#EAE8E1;padding:.1rem .35rem;font-size:.8rem}
 a{color:#8A6E33}
</style>
<main><h1>${title}</h1>${body}</main>`

export default async (request: Request, context: Context) => {
  const url = new URL(request.url)
  if (isOpen(url)) return context.next()

  const user = Deno.env.get('STAYPATH_USER')
  const pass = Deno.env.get('STAYPATH_PASS')

  // 設定前は開けない。「掛けたつもりで開いていた」を作らないため、
  // 通してしまうのではなく、何を設定すればよいかを出して止める
  // 未設定のあいだは通す。設定が済むまで運用側まで入れなくなり、
  // 実際に締め出してしまった。環境変数を入れた瞬間に下の判定が効く。
  if (!user || !pass) {
    const res = await context.next()
    res.headers.set('X-StayPath-Gate', 'off: unset')
    return res
  }


  const auth = request.headers.get('authorization') ?? ''
  if (auth.startsWith('Basic ')) {
    let decoded = ''
    try { decoded = atob(auth.slice(6)) } catch { decoded = '' }
    const at = decoded.indexOf(':')
    if (at > 0 && same(decoded.slice(0, at), user) && same(decoded.slice(at + 1), pass)) {
      return context.next()
    }
  }

  return new Response(
    page('StayPath', `
      <p>この画面は関係者だけがご覧になれます。合言葉を入力してください。</p>
      <p>お心当たりのない方は <a href="/staypath-guide">こちら</a> に
      システムの説明があります。</p>`),
    { status: 401, headers: ASK },
  )
}

export const config = { path: '/staypath/*' }
