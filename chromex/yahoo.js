// window.alert('アプリ開いたね！');
// document.getElementById

window.onload = function() {
  try {
    // テスト
    // window.alert(document.getElementsByClassName('styles_price__CD3pM')[0].innerText.replace(',', '').replace('円', ''));
    // 通常販売価格
    var price = document.getElementsByClassName('styles_price__CD3pM')[0].innerText.replace(',', '').replace('円', '');
    var point_per = get_point_per();

    float_point_per=parseFloat(point_per)*0.01
    var actual_price = parseFloat(price)-(price/1.1*float_point_per);

    // 表示領域を取得
    var ItemPrice_element = document.getElementsByClassName('styles_itemPriceArea__kVrc_ target_modules')[0];

    // 通常価格のHTML要素を作成
    var elem_price = document.createElement('div');
    elem_price.textContent = '通常価格：';
    var elem_price_input = document.createElement('input');
    elem_price_input.setAttribute("size", "2");
    elem_price_input.value = price;

    //  要素の中の末尾に挿入
    ItemPrice_element.appendChild(elem_price);
    elem_price.appendChild(elem_price_input);

    // 獲得ポイント％のHTML要素を作成
    var elem_point = document.createElement('div');
    elem_point.textContent = '獲得ポイント％：';
    var elem_point_input = document.createElement('input');
    elem_point_input.setAttribute("size", "1");
    elem_point_input.value = point_per;

    //  要素の中の末尾に挿入
    ItemPrice_element.appendChild(elem_point);
    elem_point.appendChild(elem_point_input);

    // クー値引き円のHTML要素を作成
    var elem_coupon = document.createElement('div');
    elem_coupon.textContent = 'クー値引き円：';
    var elem_coupon_input = document.createElement('input');
    elem_coupon_input.setAttribute("size", "1");
    elem_coupon_input.value = 0;
    
    //  要素の中の末尾に挿入
    ItemPrice_element.appendChild(elem_coupon);
    elem_coupon.appendChild(elem_coupon_input);

    // クー倍率％のHTML要素を作成
    var elem_coupon_per = document.createElement('div');
    elem_coupon_per.textContent = 'クー倍率％：';
    var elem_coupon_per_input = document.createElement('input');
    elem_coupon_per_input.setAttribute("size", "1");
    elem_coupon_per_input.value = 0;
    
    //  要素の中の末尾に挿入
    ItemPrice_element.appendChild(elem_coupon_per);
    elem_coupon_per.appendChild(elem_coupon_per_input);

    // 実質仕入値のHTML要素を作成
    var elem_actual_price = document.createElement('div');
    elem_actual_price.textContent = '実質仕入値：';

    ItemPrice_element.appendChild(elem_actual_price);

    const input1 = document.createElement("input");
    input1.setAttribute("type", "text");
    input1.setAttribute("size", "5");
    input1.setAttribute("id", "input1");
    input1.value = Math.round(actual_price);
    elem_actual_price.appendChild(input1);

    var button = document.createElement('input');
    button.type = 'button';
    button.id = 'submit';
    button.value = '再計算';
    button.className = 'btn';
    elem_actual_price.appendChild(button);

    button.onclick = function() {
      // 通常価格
      // actual_price = price;
      actual_price = elem_price_input.value.replace(',', '');
      // 獲得ポイント％
      point_input = elem_point_input.value;
      // クー値引き円
      coupon_input = elem_coupon_input.value;
      // クー倍率％
      coupon_per_input = elem_coupon_per_input.value;
      // 実質仕入値
      actual_price = actual_price - coupon_input;
      actual_price = actual_price - (actual_price*coupon_per_input/100);
      actual_price = actual_price-(actual_price/1.1*point_input/100);
      input1.value = Math.round(actual_price);

    };

    // 新しいHTML要素を作成
    // var new_element = document.createElement('div');
    // new_element.textContent = 'P：' + point_per + "｜" + '実質仕入値：' + Math.round(actual_price);

    // 指定した要素の中の末尾に挿入
    ItemPrice_element.appendChild(new_element);
  } catch(e) {
    console.log( e.message );
  }
}
function get_point_per() {
  // try {
  //   point_per = document.getElementsByClassName('elGetRate')[0].innerText.replace('%獲得', '');
  //   if (point_per=='') {
  //     throw new Error('not get');
  //   }
  //   return point_per
  // } catch(e) {
  //   try {
  //     point_per = document.getElementsByClassName('elGetRateText')[0].innerHTML.replace('%獲得', '');
  //     return point_per
  //   } catch(e) {
  //     return 0
  //   }
  // }

  try {
    point_per = document.getElementsByClassName('styles_pointRatio__EepZ3')[0].innerHTML.replace('<!-- -->', '').replace('%獲得', '');
    return point_per
  } catch(e) {
    return 0
  }

}
