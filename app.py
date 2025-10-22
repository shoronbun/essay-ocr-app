import streamlit as st
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="手書き小論文OCR",
    page_icon="📝",
    layout="wide"
)

# 認証情報を取得
@st.cache_resource
def get_client():
    """Document AIクライアントを取得"""
    try:
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        project_id = st.secrets["PROJECT_ID"]
        location = st.secrets["LOCATION"]
        processor_id = st.secrets["PROCESSOR_ID"]
        
        opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
        client = documentai.DocumentProcessorServiceClient(
            credentials=credentials,
            client_options=opts
        )
        return client, project_id, location, processor_id
    except:
        return None, None, None, None

client, PROJECT_ID, LOCATION, PROCESSOR_ID = get_client()

# ヘッダー
st.title("📝 手書き小論文 OCR システム")
st.caption("答案をアップロードするだけで、テキストに変換できます")

if client is None:
    st.error("❌ システムエラー：管理者に連絡してください")
    st.stop()
else:
    st.success("✅ システム稼働中")

st.markdown("---")

# OCR処理
def perform_ocr(file_bytes, file_name):
    """OCR実行"""
    try:
        name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
        
        # ファイルタイプ判定
        if file_name.lower().endswith('.pdf'):
            mime_type = "application/pdf"
        elif file_name.lower().endswith(('.jpg', '.jpeg')):
            mime_type = "image/jpeg"
        else:
            mime_type = "image/png"
        
        raw_document = documentai.RawDocument(content=file_bytes, mime_type=mime_type)
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        
        result = client.process_document(request=request)
        document = result.document
        
        stats = {
            "文字数": len(document.text),
            "ページ数": len(document.pages),
        }
        
        return document.text, stats, None
    except Exception as e:
        return None, None, str(e)

# メイン画面
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 ファイルをアップロード")
    uploaded_file = st.file_uploader(
        "答案の画像またはPDFを選択",
        type=['jpg', 'jpeg', 'png', 'pdf']
    )
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")
        if not uploaded_file.name.lower().endswith('.pdf'):
            st.image(uploaded_file, use_container_width=True)

with col2:
    st.subheader("🚀 テキスト化")
    
    if uploaded_file:
        if st.button("📝 OCR実行", type="primary", use_container_width=True):
            with st.spinner("処理中..."):
                text, stats, error = perform_ocr(
                    uploaded_file.getvalue(),
                    uploaded_file.name
                )
                
                if error:
                    st.error(f"❌ エラー: {error}")
                else:
                    st.success("✅ 完了！")
                    st.session_state['result'] = text
                    st.session_state['stats'] = stats
                    st.session_state['file'] = uploaded_file.name

# 結果表示
if 'result' in st.session_state:
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("文字数", f"{st.session_state['stats']['文字数']:,}")
    with col2:
        st.metric("ページ数", st.session_state['stats']['ページ数'])
    with col3:
        st.download_button(
            "📥 ダウンロード",
            st.session_state['result'],
            f"ocr_{st.session_state['file']}.txt",
            use_container_width=True
        )
    
    st.text_area(
        "認識結果",
        st.session_state['result'],
        height=400
    )

# 使い方
with st.expander("📖 使い方"):
    st.markdown("""
    1. 答案の写真を撮影するか、スキャンする
    2. 上のボックスにファイルをドラッグ＆ドロップ
    3. 「OCR実行」ボタンをクリック
    4. テキストを確認してダウンロード
    
    **高精度のコツ**：
    - 明るい場所で撮影
    - 真上から撮影
    - ピントを合わせる
    """)
```

4. 一番下までスクロールして「**Commit changes**」をクリック

## 3-4. ファイルを作成（その2：requirements.txt）

1. 「**Add file**」→ 「**Create new file**」

2. ファイル名：
```
   requirements.txt
```

3. 以下をコピー&ペースト：
```
   streamlit==1.31.0
   google-cloud-documentai==2.24.0
```

4. 「**Commit changes**」をクリック

## 3-5. ファイルを作成（その3：.streamlit/config.toml）

1. 「**Add file**」→ 「**Create new file**」

2. ファイル名（**スラッシュも含めて**）：
```
   .streamlit/config.toml
