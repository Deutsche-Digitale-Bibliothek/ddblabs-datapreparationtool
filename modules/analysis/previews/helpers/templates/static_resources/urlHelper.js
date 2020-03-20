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

/**
 * Initialize the history support for the search page(s)
 *
 * @param stateManager callback triggered on history state changes
 */
de.ddb.common.search.initHistorySupport = function(stateManager) {
  if (window.history && history.pushState) {
    historyedited = false;
    historySupport = true;
    $(window).bind('popstate', function() {
      if (historyedited) {
        stateManager(location.pathname + location.search);
      }
    });
  } else {
    historySupport = false;
    // Utilized for browser that doesn't supports pushState.
    // It will be used as reference URL for all the ajax actions
    globalUrl = location.search.substring(1);
  }
};

/**
 * Adds new paths to the history
 *
 * @param path the path to add to the history
 */
de.ddb.common.search.historyManager = function(path) {
  if (historySupport) {
    window.history.pushState({
      path : path
    }, '', path);
    historyedited = true;
  } else {
    globalUrl = (path.indexOf('?') > -1) ? path.split('?')[1] : path;
    window.location = path;
  }
};

/**
 * Gets all request params from the window url that starts with facetValues[]
 */
de.ddb.common.search.getFacetValuesFromUrl = function() {
  var facetValuesFromUrl = de.ddb.common.search.getUrlVar('facetValues%5B%5D');
  if (facetValuesFromUrl == null) {
    facetValuesFromUrl = de.ddb.common.search.getUrlVar('facetValues[]');
  }

  return facetValuesFromUrl;
};

/**
 * Adds a new facetValue to the facetValues[] params of the window url.
 * An offset param is added to this list too. So a new search request can be performed based on the updated facetValues[] params
 *
 * Returns an array with request params for a new facet based search
 */
de.ddb.common.search.addFacetValueToParams = function(facetField, facetValue) {
  var paramsFacetValues = de.ddb.common.search.getFacetValuesFromUrl();

  //The facet values will be stored in a two dimensional Array ["facetValues[]",['type_fctyDmediatype_003','time_begin_fct=1014', 'time_end_fct=2014',]]
  var paramsArray = null;

  if (paramsFacetValues) {
    $.each(paramsFacetValues, function(key, value) {
      paramsFacetValues[key] = decodeURIComponent(value.replace(/\+/g, '%20'));
    });
    paramsFacetValues.push(facetField + '=' + facetValue);
    paramsArray = [['facetValues[]', paramsFacetValues]];
  } else {
    paramsArray = [['facetValues[]', facetField + '=' + facetValue]];
  }

  paramsArray.push(['offset', 0]);

  return paramsArray;
};

/**
 * Returns an array with url params that match the given name
 */
de.ddb.common.search.getUrlVar = function(name) {
  return de.ddb.common.search.getUrlVars()[name];
};

/**
 * Returns an array with the url params
 */
de.ddb.common.search.getUrlVars = function() {
  var vars = {}, hash;

  if (typeof historySupport !== "undefined") {
    var hashes = (historySupport) ? window.location.href.slice(
        window.location.href.indexOf('?') + 1).split('&') : globalUrl.split('&');
    for ( var i = 0; i < hashes.length; i++) {
      hash = hashes[i].split('=');
      if (!Object.prototype.hasOwnProperty.call(vars, hash[0])) {
        vars[hash[0]] = [];
      }
      vars[hash[0]].push(hash[1]);
    }
  }
  return vars;
};

de.ddb.common.search.getParameterByName = function (name) {
  name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
  results = regex.exec(location.search);
  return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
};
