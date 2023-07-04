# OCR-Sample
 Easy OCRを使った文字認識サンプルアプリの制作

## 環境構築
### 実行環境
- Python 3.10.4
- pyenv  2.3.1
- macOS Ventura 13.3.1 (a)

以上の環境を前提とします。
### 初期設定
1. pyenvのインストール
Pythonのバージョン管理ツールであるpyenvをインストールします。
```bash
brew install pyenv

※windowsの場合はchocolateyを使うと楽です。
choco install pyenv-win
```

2. Pythonのインストール
pyenvを使ってPythonをインストールします。
```bash
pyenv install 3.10.4
pyenv rehash
```

3. 仮想環境の作成と有効化
まずローカルのpython環境を固定します。
```bash
pyenv local 3.10.4
```
仮想環境を作成します。
```bash
python -m venv .venv
```
.venvディレクトリに仮想環境が作成されます。

仮想環境を有効化します。
```bash
source .venv/bin/activate

※ Windows PowerShellの場合
.venv/Scripts/Activate.ps1
```

これで仮想環境が有効化され、プロンプトの先頭に(.venv)が表示されます。
```bash
(.venv) $
```

4. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```


## 実行方法
```bash
python -m OCR-Sample
```

