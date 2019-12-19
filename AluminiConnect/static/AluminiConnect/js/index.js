/*  
    FOR FUTURE USE

    this file is for handling card height of events,news,gallery in homepage. 
    this script gets the height of images of the cards, 
    calculates its average and applies average height to the cards 

    for now, this is not included in the project as card-image height is fixed
*/ 


function event_cards() {
  var event_cards = document.getElementsByClassName('event-card-img');
  var event_cards_height_sum = 0;
  var x = 0;
  for (var i=0; i < event_cards.length; i++) {
      var h = parseInt(window.getComputedStyle(event_cards[i], null).getPropertyValue('height'), 10);
      event_cards_height_sum += h;
      if (h > 0) 
        x++;
  }
  var event_cards_height_avg = event_cards_height_sum / x;
  for (var i=0; i < event_cards.length; i++) {
      event_cards[i].style.height = event_cards_height_avg + "px";
  }
}

function news_cards() {
  var news_cards = document.getElementsByClassName('news-card-img');
  var news_cards_height_sum = 0;
  var x = 0;
  for (var i=0; i < news_cards.length; i++) {
      var h = parseInt(window.getComputedStyle(news_cards[i], null).getPropertyValue('height'), 10);
      news_cards_height_sum += h;
      if (h > 0) 
        x++;
  }
  var news_cards_height_avg = news_cards_height_sum / x;
  for (var i=0; i < news_cards.length; i++) {
      news_cards[i].style.height = news_cards_height_avg + "px";
  }
}

function gallery_cards() {
  var gallery_cards = document.getElementsByClassName('gallery-card-img');
  var gallery_cards_height_sum = 0;
  var x = 0;
  for (var i=0; i < gallery_cards.length; i++) {
      var h = parseInt(window.getComputedStyle(gallery_cards[i], null).getPropertyValue('height'), 10);
      gallery_cards_height_sum += h;
      if (h > 0) 
        x++;
  }
  var gallery_cards_height_avg = gallery_cards_height_sum / x;
  for (var i=0; i < gallery_cards.length; i++) {
      gallery_cards[i].style.height = gallery_cards_height_avg + "px";
  }
}