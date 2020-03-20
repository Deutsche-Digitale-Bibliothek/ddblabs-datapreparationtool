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

// Trim of the given text to the passed chars limit
$.cutoffStringAtSpace = function(text, limit) {
  if (text != null && text.toString().length > limit) {
    return $.trim(text.toString()).substring(0, limit).split(" ").slice(0, -1).join(" ") + "...";
  }
  return text;
};

$.browser={ msie: navigator.appName === 'Microsoft Internet Explorer' };

// Initialization of the JWPlayer
$.initializeJwPlayer = function(divId, videoFile, previewImage, width, height, onReadyCallback, onErrorCallback) {
  jwplayer(divId).setup({
    'flashplayer' : jsContextPath + '/js/vendor/jwplayer-6.2.3115/jwplayer.flash.swf',
    'html5player' : jsContextPath + '/js/vendor/jwplayer-6.2.3115/jwplayer.html5.js',
    'modes' : [ {
      type : "html5",
      src : jsContextPath + "/js/vendor/jwplayer-6.2.3115/jwplayer.html5.js"
    }, {
      type : "flash",
      src : jsContextPath + "/js/vendor/jwplayer-6.2.3115/jwplayer.flash.swf"
    }, {
      type : "download"
    } ],
    'fallback' : true,
    'autostart' : false,
    'file' : videoFile,
    'skin' : jsContextPath + '/js/vendor/jwplayer-6.2.3115/skins/five.xml',
    'image' : previewImage,
    'controls' : true,
    'controlbar' : 'bottom',
    'stretching' : 'uniform',
    'width' : width,
    'height' : height,
    'primary' : 'html5',
    'startparam' : 'starttime',
    'events' : {
      onError : onErrorCallback,
      onReady : onReadyCallback
    }
  });
};
/**
 * This function will give you back the current url (if no urlParameters is setted) plus the new parameters added
 * IMPORTANT: remember to pass your arrayParamVal already URL decoded
 */
$.addParamToCurrentUrl = function(arrayParamVal, urlString) {
  return $.addParamToCurrentUrlWithHistorySupport(arrayParamVal, urlString);
};

/**
 * This function will give you back the current url (if no urlParameters is setted) plus the new parameters added
 * The methods checks for the global attribute historySupport.
 *
 * IMPORTANT: remember to pass your arrayParamVal already URL decoded
 */
$.addParamToCurrentUrlWithHistorySupport = function(arrayParamVal, urlString) {
  var currentUrl = (historySupport) ? location.search.substring(1) : globalUrl;

  return $.addParamToUrl(currentUrl,arrayParamVal, null, urlString, true);
};

/**
 * Adds the given params to the given url
 */
$.addParamToUrl = function(currentUrl, arrayParamVal, path, urlString, updateLanguage) {
  var queryParameters = {}, queryString = (urlString == null) ? currentUrl : urlString, re = /([^&=]+)=([^&]*)/g, m;
  while (m = re.exec(queryString)) {
    var decodedKey = decodeURIComponent(m[1].replace(/\+/g, '%20'));
    if (queryParameters[decodedKey] == null) {
      queryParameters[decodedKey] = [];
    }
    queryParameters[decodeURIComponent(m[1].replace(/\+/g, '%20'))].push(decodeURIComponent(m[2]
        .replace(/\+/g, '%20')));
  }
  $.each(arrayParamVal, function(key, value) {
    queryParameters[value[0]] = value[1];
  });
  var tmp = jQuery.param(queryParameters, true);

  //Update the language switch
  if (updateLanguage) {
    $.updateLanguageSwitch(tmp);
  }

  if (path == null) {
    return window.location.pathname + '?' + tmp;
  } else {
    return path + '?' + tmp;
  }
};

/**
 * Removes an array of params from the given url
 */
$.removeParamFromUrl = function(arrayParamVal, path, urlString) {
  var currentUrl = (historySupport) ? location.search.substring(1) : globalUrl;
  var queryParameters = {}, queryString = (urlString == null) ? currentUrl : urlString, re = /([^&=]+)=([^&]*)/g, m;
  while (m = re.exec(queryString)) {
    var keyParam = decodeURIComponent(m[1].replace(/\+/g, '%20'));
    if (queryParameters[keyParam] == null) {
      queryParameters[keyParam] = [];
    }
    queryParameters[keyParam].push(decodeURIComponent(m[2].replace(/\+/g, '%20')));
  }
  $.each(arrayParamVal, function(key, value) {
    if (queryParameters[value[0]]
        && (paramIndex = $.inArray(value[1], queryParameters[value[0]])) > -1) {
      queryParameters[value[0]] = jQuery.grep(queryParameters[value[0]], function(cValue) {
        return cValue !== value[1];
      });
    }
  });
  var tmp = jQuery.param(queryParameters, true);
  $.updateLanguageSwitch(tmp);
  if (path == null) {
    return window.location.pathname + '?' + tmp;
  } else {
    return path + '?' + tmp;
  }
};

/**
 * Update the language switch link for the given params
 */
$.updateLanguageSwitch = function(params) {
  params = params.replace(/\&?lang=[^\&]*/g, '');
  if (params.length > 0) {
    params += '&';
  }
  if (params.indexOf('&') === 0) {
    params = params.substring(1);
  }
  var pattern = /(.*?\?).*?(lang=\w*)/;
  $('.language-wrapper .selector').find('a[href]').each(function() {
    var matches = pattern.exec($(this).attr('href'));
    $(this).attr('href', matches[1] + params + matches[2]);
  });
};

$(window).on('load', function () {

  // hide search field in mobile view when menu is open
  var mobileMenuButton = $('.index-nav button');

  if (mobileMenuButton) {
    mobileMenuButton.click(function() {
      if ($('#mobileMenu').height() > 0) {
        $('.mobile-search-field').removeClass("off");
      }
      else {
        $('.mobile-search-field').addClass("off");
      }
    });
  }

});

/**
 * This function will initialize the popover for the glossary definitions
 */
$.initWordsDefinitions = function() {
  $('.glossaryTerm').popover();
};
