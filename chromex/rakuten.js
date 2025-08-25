// window.alert('アプリ開いたね！');
// document.getElementById

window.onload = function() {
  try {
    // 通常販売価格
    var price = document.getElementById('priceCalculationConfig').getAttribute("data-price");
    var point_per = parseFloat(get_point_per());
    var spu = 3;
    
    float_point_per = point_per * 0.01;
    float_spu = spu * 0.01;
    var actual_price = parseFloat(price)-(price/1.1*(float_point_per+float_spu));
    // 表示領域を取得
    var ItemPrice_element = document.getElementById('priceCalculationConfig');
    
    // spuのHTML要素を作成
    var elem_spu = document.createElement('div');
    elem_spu.textContent = 'SPU：　　　';
    var elem_spu_input = document.createElement('input');
    elem_spu_input.setAttribute("size", "1");
    elem_spu_input.value = spu;

    //  要素の中の末尾に挿入
    ItemPrice_element.appendChild(elem_spu);
    elem_spu.appendChild(elem_spu_input);

    // 獲得ポイント％のHTML要素を作成
    var elem_point = document.createElement('div');
    elem_point.textContent = '獲得ポイント％：';
    var elem_point_input = document.createElement('input');
    elem_point_input.setAttribute("size", "1");
    elem_point_input.setAttribute("id", "basic_point");
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
    input1.setAttribute("id", "actual_price");
    input1.value = Math.round(actual_price);
    elem_actual_price.appendChild(input1);

    var button = document.createElement('input');
    button.type = 'button';
    button.id = 'submit';
    button.value = '再計算';
    button.className = 'btn';
    elem_actual_price.appendChild(button);

    button.onclick = function() {
      actual_price = price;
      // SPU
      spu_input = parseFloat(elem_spu_input.value)
      // 獲得ポイント％
      point_input = parseFloat(elem_point_input.value);
      // クー値引き円
      coupon_input = elem_coupon_input.value;
      // クー倍率％
      coupon_per_input = elem_coupon_per_input.value;
      // 実質仕入値
      actual_price = actual_price - coupon_input;
      actual_price = actual_price - (actual_price*coupon_per_input/100);
      actual_price = actual_price-(actual_price/1.1*(spu_input + point_input)/100);
      input1.value = Math.round(actual_price);
      
    };

  } catch(e) {
    console.log( e.message );
  }
}

function get_point_per() {
  try {
    point_per = document.querySelector('#rakutenLimitedId_cart > tbody > tr:nth-child(1) > div:nth-child(2) > div > div:nth-child(4) > div > div > ul.point-summary__campaign___2KiT-.point-summary__multiplier-up___3664l.point-up > li:nth-child(2)').innerText.replace('倍UP', '');
    return point_per
  } catch(e) {
    try {
      point_per = document.querySelector('#rakutenLimitedId_cart > tbody > tr:nth-child(3) > td > div > div > ul.point-summary__campaign___2KiT-.point-summary__multiplier-up___3664l.point-up > li:nth-child(2)').innerText.replace('倍UP', '');
      return point_per
    } catch(e) {
      try {
        point_per = document.querySelector('#rakutenLimitedId_cart > tbody > tr:nth-child(3) > td > div > div > ul.point-summary__campaign___2KiT-.point-summary__rebate___OwnwU.point-superdeal > li:nth-child(2)').innerText.replace('%ポイントバック', '');
        point_per = parseInt(point_per)-1;
        return point_per
      } catch(e) {
        try {
          point_per = document.querySelector('#rakutenLimitedId_cart > tbody > tr:nth-child(2) > td > div > div > ul.point-summary__campaign___2KiT-.point-summary__rebate___OwnwU.point-superdeal > li:nth-child(2)').innerText.replace('%ポイントバック', '');
          point_per = parseInt(point_per)-1;
          return point_per
        } catch(e) {
          return 0
        }
      }
    }
  }
}

