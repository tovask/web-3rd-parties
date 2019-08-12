log = console.log

var buttonKeywords = [
  'rendben',
  'elfogad',
  'confirm',
  'folytat',
  'értettem',
];

function isVisibleInViewport(element){
  const rect = element.getBoundingClientRect();
  if(rect.width==0 || rect.height==0){
    return false;
  }
  if(0>rect.bottom || 0>rect.right){
    return false;
  }
  if(rect.top > Math.max(document.documentElement.clientHeight, window.innerHeight)){
    return false;
  }
  if(rect.left > Math.max(document.documentElement.clientWidth, window.innerWidth)){
    return false;
  }
  return true;
}

function isButtonText(node){
  let text = node.data.trim();
  if( text.length>50 || ! /\S/.test(text) ){
    return false;
  }

  if(!isVisibleInViewport(node.parentElement)){
    return false;
  }

  text = text.toLowerCase();

  for(const keyword of buttonKeywords){
    if(text.indexOf(keyword) != -1){
      return true;
    }
  }

  if(text == 'ok' || text == 'oké' || text == 'oké!'){
    return true;
  }

  /* if(text == '×'){ // passive close button
      return true;
    } */

  return false;
}

function findBestButton(textNodes){
  let best;

  if( (best = textNodes.find(textNode => textNode.parentElement.className.includes('btn')) ) ){
    // cc_btn cc_btn_accept_all
    return best;
  }

  if( (best = textNodes.find(textNode => textNode.data.trim().toLowerCase()=='ok') ) ){
    return best;
  }

  return textNodes[0];
}

function getButtonTextNode() {
  var walker = document.createTreeWalker(
    document.body, 
    NodeFilter.SHOW_TEXT, 
    {
      acceptNode: function(node) {
        if ( isButtonText(node) ) {
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    },
  );

  var node;
  var textNodes = [];
  while(node = walker.nextNode()) {
    textNodes.push(node);
  }

  log(textNodes);
  
  if (textNodes.length>1) {
    return findBestButton(textNodes).parentElement;
  } else if (textNodes[0]) {
    return textNodes[0].parentElement;
  }
}

window.gdpr_concern_button = getButtonTextNode();

log( window.gdpr_concern_button )

if( window.gdpr_concern_button ) {
	// window.gdpr_concern_button.click(); // close the banner
}
