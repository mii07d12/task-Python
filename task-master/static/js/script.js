document.addEventListener('DOMContentLoaded', function () {
    // モーダルの動作
    const modal = document.getElementById('descriptionModal');
    const modalContent = document.getElementById('descriptionText');
    const closeBtn = document.querySelector('.close');

    // 説明ボタンのクリックイベント
    document.querySelectorAll('.show-description').forEach(button => {
        button.addEventListener('click', function () {
            const description = this.getAttribute('data-description');
            modalContent.textContent = description || '説明はありません。';
            modal.style.display = 'block';
        });
    });

    // モーダルを閉じる
    closeBtn.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // モーダル外をクリックして閉じる
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // カラーピッカーの初期化とイベント
    const colorPicker = document.getElementById('colorPicker');
    const resetColorButton = document.getElementById('resetColorButton');

    // ページの読み込み時にローカルストレージから色を取得して反映
    const savedColor = localStorage.getItem('accentColor'); // ローカルストレージから色を取得
    if (savedColor) {
        // 保存されていた色をカラーピッカーに反映
        colorPicker.value = savedColor;
        // ページの差し色を設定
        document.documentElement.style.setProperty('--accent-color', savedColor);
    }

    // カラーピッカーで色が変更された時のイベントリスナー
    colorPicker.addEventListener('input', function () {
        const selectedColor = colorPicker.value; // ユーザーが選んだ色
        localStorage.setItem('accentColor', selectedColor); // ローカルストレージに選択した色を保存
        document.documentElement.style.setProperty('--accent-color', selectedColor); // :root にある --accent-color を更新
    });

    // デフォルト色に戻すボタンのクリックイベント
    resetColorButton.addEventListener('click', function () {
        const defaultColor = '#ADD8E6'; // デフォルト色
        colorPicker.value = defaultColor; // カラーピッカーをデフォルト色に戻す
        localStorage.removeItem('accentColor'); // ローカルストレージから削除
        document.documentElement.style.setProperty('--accent-color', defaultColor); // ページの差し色をデフォルト色に設定
    });

    // テーマ切り替え用のイベント
    const themeLink = document.getElementById('theme-link'); // <link>タグを取得
    const themeRadios = document.querySelectorAll('input[name="theme"]');

    // ラジオボタンが変更されたときのイベント
    themeRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.value === 'dark') {
                themeLink.href = '/static/css/dark-theme.css'; // ダークテーマを適用
            } else if (this.value === 'light') {
                themeLink.href = '/static/css/light-theme.css'; // ライトテーマを適用
            }
        });
    });

    // ページの読み込み時にローカルストレージのテーマを適用
    const savedTheme = localStorage.getItem('theme'); // テーマの状態を取得
    if (savedTheme) {
        themeLink.href = `/static/css/${savedTheme}-theme.css`; // 保存されていたテーマを適用
        document.querySelector(`input[value="${savedTheme}"]`).checked = true; // 該当ラジオボタンを選択
    } else {
        themeLink.href = '/static/css/dark-theme.css'; // デフォルトはダークテーマ
        document.querySelector('input[value="dark"]').checked = true; // ダークテーマのラジオボタンを選択
    }

    // ラジオボタンの変更時にテーマを保存
    themeRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            const selectedTheme = this.value; // 選択されたテーマを取得
            localStorage.setItem('theme', selectedTheme); // テーマをローカルストレージに保存
        });
    });
});
