// window.alert('アプリ開いたね！');
// document.getElementById

window.onload = function() {
  try {
    
    // 通常販売価格
    // var price = document.getElementsByClassName('Price_price__currentPrice__FaSZR false')[0].innerText.replace(',', '').replace('円(税込)', '');
    var price = get_price();
    var point_per = document.getElementsByClassName('ReductionDetails_reduction__contents_rate__GEFFj')[0].innerText.replace('(', '').replace('%)', '');
    point_per = point_per.replace(',', '');

    float_point_per=parseFloat(point_per)*0.01
    var actual_price = parseFloat(price)-(price/1.1*float_point_per);
    

    // 表示領域を取得
    var ItemPrice_element = document.getElementsByClassName('Price_price__HskDt')[0];

    // 獲得ポイント％のHTML要素を作成
    var elem_point = document.createElement('div');
    elem_point.textContent = '獲得ポイント％：';
    var elem_point_input = document.createElement('input');
    elem_point_input.setAttribute("size", "1");
    elem_point_input.setAttribute("id", "basic_point");
    elem_point_input.value = point_per;
    elem_point_input.setAttribute("value", point_per);

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
    input1.setAttribute("id", "actual_price");
    input1.value = Math.round(actual_price);
    input1.setAttribute("value", actual_price);
    elem_actual_price.appendChild(input1);

    var button = document.createElement('input');
    button.type = 'button';
    button.id = 'submit';
    button.value = '再計算';
    button.className = 'btn';
    elem_actual_price.appendChild(button);

    button.onclick = function() {
      actual_price = price;
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
};

function get_price() {
  try {
    price = document.getElementsByClassName('Price_price__currentPrice__FaSZR false')[0].innerText.replace(',', '').replace('円(税込)', '');
    return price
  } catch(e) {
    try {
      price = document.getElementsByClassName('Price_price__currentPrice__FaSZR Price_price__currentPrice_sale__tmcHk')[0].innerText.replace(',', '').replace('円(税込)', '');
      return price
    } catch(e) {
      return 0
    }
  }
}

