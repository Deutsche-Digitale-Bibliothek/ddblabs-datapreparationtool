/*
 * Copyright (C) 2014 FIZ Karlsruhe
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

//Gets the parameters from a URL
function getUrlParam(name){
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.hash);

  if(results === null) {
    results = regex.exec(window.location.search);
  }

  if(results === null) {
    return "";
  }else{
    return decodeURIComponent(results[1].replace(/\+/g, " "));
  }
}

/**
 * Returns an array with url params that match the given name
 */
$.getUrlVar = function(name) {
  return $.getUrlVars()[name];
};

/**
 * Returns an array with the url params
 */
$.getUrlVars = function() {
  var vars = {}, hash;
  var hashes = (historySupport) ? window.location.href.slice(
      window.location.href.indexOf('?') + 1).split('&') : globalUrl.split('&');
  for ( var i = 0; i < hashes.length; i++) {
    hash = hashes[i].split('=');
    if (!Object.prototype.hasOwnProperty.call(vars, hash[0])) {
      vars[hash[0]] = [];
    }
    vars[hash[0]].push(hash[1]);
  }
  return vars;
};

/**
 * Toggle the element specified in the attribute data-filters
 */
$.toggleElement = function() {
  $( "a[data-filters]" ).click(function(event) {
    event.preventDefault();
    var that = this;
    var elementToToggle = $(this).attr("data-filters");
    $(elementToToggle).slideToggle(400, function(){
      var icon = $(that).find("i");
      if(icon.hasClass("icon-chevron-down")){
        icon.removeClass("icon-chevron-down");
        icon.addClass("icon-chevron-up");
      }else{
        icon.removeClass("icon-chevron-up");
        icon.addClass("icon-chevron-down");
      }
    });
  });
};


/**
 * update a jQuery object stored in a variable after DOM change
 */
$.fn.update = function(){
  var newElements = $(this.selector),i;
  for(i=0;i<newElements.length;i++){
    this[i] = newElements[i];
  }
  for(;i<this.length;i++){
    this[i] = undefined;
  }
  this.length = newElements.length;
  return this;
};

/**
 * Check if is a mobile view
 */
$.isMobile = function() {
  return (screen.width <= 767) ||
  (window.matchMedia &&
      window.matchMedia('only screen and (max-width: 767px)').matches
   );
};

/**
 * Add missing function for IE 11.
 */
if (!String.prototype.startsWith) {
  String.prototype.startsWith = function(searchString, position) {
    position = position || 0;
    return this.indexOf(searchString, position) === position;
  };
}