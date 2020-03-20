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

/* Search namespace  */
de.ddb.common.search = de.ddb.common.search || {};

var COOKIENAME = "searchParameters";

/**
 * Create a JSON object from the search cookie content.
 */
de.ddb.common.search.parseCookie = function() {
  var result = {};
  var searchParameters = de.ddb.common.search.readCookie(COOKIENAME + jsContextPath);

  if (searchParameters) {
    searchParameters = searchParameters.substring(1, searchParameters.length - 1);
    searchParameters = searchParameters.replace(/\\"/g, '"');
    result = $.parseJSON(searchParameters);
  }
  return result;
}

/**
 * Create a json cookie of search parameters to the current context path
 * @param arrayParamVal array of parameters values
 */
de.ddb.common.search.setSearchCookieParameter = function(arrayParamVal) {
  var path = '/';
  var json = de.ddb.common.search.parseCookie();

  $.each(arrayParamVal, function(key, value) {
    if (value[1].constructor === Array) {
      for (var i = 0; i < value[1].length; i++) {
        if (value[1][i].constructor === String) {
          value[1][i] = encodeURIComponent(value[1][i]).replace(/%20/g, '\+');
        }
      }
    }
    else if (value[1].constructor === String) {
      value[1] = encodeURIComponent(value[1]).replace(/%20/g, '\+');
    }
    json[value[0]] = value[1];
  });
  document.cookie = COOKIENAME + jsContextPath + "=\"" + JSON.stringify(json).replace(/"/g, '\\"') + "\"" + ';path=' + path;
};

/**
 * Remove a specific value into the search parameter cookie of the current context path.
 * @paramName name of the parameter to remove
 * @value value of the parameter to remove
 */
de.ddb.common.search.removeCookieParameterValue = function(paramName, value) {
  var path = '/';
  var valueDecode = decodeURIComponent(value.replace(' ', '+'));
  var json = de.ddb.common.search.parseCookie();

  $.each(json, function(key, jsonValue) {
    if(key === paramName) {
      if(jsonValue.constructor === Array) {
        $.each(jsonValue, function(arrayKey, arrayValue) {
          if(valueDecode === arrayValue) {
            var index = jsonValue.indexOf(arrayValue);
            jsonValue.splice(index, 1);;
          }
        });
      }else {
        if (decodeURIComponent(value.replace(' ', '+')) === jsonValue) {
          delete json[paramName];
        }
      }
    }
  });
  document.cookie = COOKIENAME + jsContextPath + "=\"" + JSON.stringify(json).replace(/"/g, '\\"') + "\"" + ';path=' + path;
};

/**
 * Remove a whole parameter of the search parameter cookie of the current context path
 * @paramName name of the parameter to remove
 */
de.ddb.common.search.removeSearchCookieParameter = function(paramName) {
  var path = '/';
  var json = de.ddb.common.search.parseCookie();

  //deletes the attribute from the JSON
  delete json[paramName];
  document.cookie = COOKIENAME + jsContextPath + "=\""
      + JSON.stringify(json).replace(/"/g, '\\"') + "\"" + ';path=' + path;
};

/**
 * Return a specific cookie if this exits
 * @name Name of the cookie to read
 */
de.ddb.common.search.readCookie = function(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for ( var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1, c.length);
    }
    if (c.indexOf(nameEQ) === 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
};