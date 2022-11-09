// window.alert('アプリ開いたね！');
// document.getElementById

window.onload = function() {
    // 通常販売価格
    var actual = document.getElementsByClassName('ItemPrice_price')[0].innerText;
    // 表示領域を取得
    var ItemPrice_element = document.getElementsByClassName('ItemPrice')[0];
    // 新しいHTML要素を作成
    var new_element = document.createElement('div');
    new_element.textContent = '実質仕入値：' + actual;

    // 指定した要素の中の末尾に挿入
    ItemPrice_element.appendChild(new_element);
  };





