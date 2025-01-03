// JSONファイルを読み込み、HTMLに表示するプログラム

document.addEventListener("DOMContentLoaded", () => {
    const jsonFilePath = "data.json"; // JSONファイルのパス

    // JSONファイルを取得する関数
    fetch(jsonFilePath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            displayData(data);
        })
        .catch(error => {
            console.error("Error loading JSON file:", error);
        });

    // データをHTMLに表示する関数
    function displayData(data) {
        const container = document.getElementById("json-display");

        // タイトル
        const titleElement = document.createElement("h1");
        titleElement.textContent = data.title;
        container.appendChild(titleElement);

        // 日本語の文章
        const japaneseElement = document.createElement("p");
        japaneseElement.textContent = `日本語: ${data.original_japanese}`;
        container.appendChild(japaneseElement);

        // ユーザーの英訳
        const userTranslationElement = document.createElement("p");
        userTranslationElement.textContent = `ユーザーの英訳: ${data.user_translation}`;
        container.appendChild(userTranslationElement);

        // 修正された英訳
        const correctedTranslationElement = document.createElement("p");
        correctedTranslationElement.textContent = `修正された英訳: ${data.corrected_translation}`;
        container.appendChild(correctedTranslationElement);

        // エラーと理由
        if (data.errors && data.errors.length > 0) {
            const errorsElement = document.createElement("ul");
            errorsElement.textContent = "エラー一覧:";
            data.errors.forEach(error => {
                const errorItem = document.createElement("li");
                errorItem.textContent = `${error.error} - ${error.reason}`;
                errorsElement.appendChild(errorItem);
            });
            container.appendChild(errorsElement);
        }

        // スコア
        const scoreElement = document.createElement("p");
        scoreElement.textContent = `スコア: ${data.score.value} (${data.score.explanation})`;
        container.appendChild(scoreElement);

        // 改善のアドバイス
        if (data.suggestions && data.suggestions.length > 0) {
            const suggestionsElement = document.createElement("ul");
            suggestionsElement.textContent = "改善のアドバイス:";
            data.suggestions.forEach(suggestion => {
                const suggestionItem = document.createElement("li");
                suggestionItem.textContent = suggestion;
                suggestionsElement.appendChild(suggestionItem);
            });
            container.appendChild(suggestionsElement);
        }

        // 知っておくとよい単語やフレーズ
        if (data.words && data.words.length > 0) {
            const wordsElement = document.createElement("ul");
            wordsElement.textContent = "知っておくとよい単語やフレーズ:";
            data.words.forEach(wordObj => {
                const wordItem = document.createElement("li");
                wordItem.textContent = `${wordObj.word}: ${wordObj.definition}`;
                wordsElement.appendChild(wordItem);
            });
            container.appendChild(wordsElement);
        }
    }
});
