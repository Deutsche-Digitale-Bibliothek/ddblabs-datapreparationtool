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
de.ddb.apd.search = de.ddb.apd.search || {};

/**
 * State Manager
 *
 * The main intend of this object is to handle the state of the structure and object page.
 * The state is defined by the selected filter and facet values as well as pagination parameters like rows, offset and sort.
 *
 * The state is stored as query parameters in the browser url
 * To read and manipulate the browser url
 *
 */
de.ddb.apd.search.StateManager = function() {
  this.init();
};

/**
 * Extend the prototype of the StateManager with jQuery
 */
$.extend(de.ddb.apd.search.StateManager.prototype, {

  // constants
  CONTEXT : 'context',
  PROVIDER_ID : 'provider_id',

  historyChange : false,

  urlManager : null,

  //List of Callback methods that will be invoked if the history has been changed.
  historyCallbackListener : [],

  //List of Callback methods that will be invoked if the state has been changed.
  stateChangeCallbackListener : [],

  /**
   * Initialize the new instance.
   */
  init : function() {
    var currObjInstance = this;
    currObjInstance.urlManager = new de.ddb.apd.search.UrlManager();

    var historyManager = function() {
      currObjInstance.historyChange = true;
      if (currObjInstance.historyCallbackListener) {

        //Invoke the callback functions of the controllers that want to be notified
        $.each( currObjInstance.historyCallbackListener, function(index, func) {
          func();
        });
      }

      currObjInstance.historyChange = false;

      currObjInstance.stateChanged();
    };

    currObjInstance.initHistorySupport(historyManager);
    currObjInstance.updateUrlButton();
  },

  /**
   * Initialize the history support for the search page(s)
   *
   * @param historyManager callback triggered on history state changes
   */
  initHistorySupport : function(historyManager) {
    if (window.history && history.pushState) {
      historySupport = true;
      $(window).bind('popstate', function() {
        var url = location.pathname + location.search;
        historyManager(url);
      });
    } else {
      historySupport = false;
      // Utilized for browser that doesn't supports pushState.
      // It will be used as reference URL for all the ajax actions
      globalUrl = location.search.substring(1);
    }
  },

  /**
   * Returns all filter values
   */
  getFilters : function() {
    var currObjInstance = this;
    var filters = currObjInstance.urlManager.getFilters();

    return filters ? filters : [];
  },

  /**
   * Persist a given filter value
   *
   * @param name the name of the filter
   * @param value the value of the filter
   */
  setFilter : function(name, value, docallback) {
    var currObjInstance = this;
    var written = false;

    if (!currObjInstance.hasFilter(name, value)) {
      //APD-620 Object page: remove context facet on archive filter change
      currObjInstance.removeContextFacet(false);
      currObjInstance.removeProviderIdFacet(false);

      var newUrl = currObjInstance.urlManager.setFilter(name, value);

      currObjInstance.stateChanged(newUrl, docallback);
      written = true;
    }
    return written;
  },

  /**
   * Checks if the stateManger already handle a filterValue
   *
   * @param name the name of the filter
   * @param value the value of the filter
   */
  hasFilter : function(name, value) {
    var currObjInstance = this;
    var hasFilter = currObjInstance.urlManager.hasFilter(name, value);

    return hasFilter;

  },

  /**
   * Removes a given filter value
   *
   * @param name the name of the filter
   * @param value the value of the filter
   */
  removeFilter : function(name, value, docallback) {
    var currObjInstance = this;
    var deleted = false;

    if (currObjInstance.hasFilter(name, value)) {
      //APD-620 Object page: remove context facet on archive filter change
      currObjInstance.removeContextFacet(false);
      currObjInstance.removeProviderIdFacet(false);

      var newUrl =  currObjInstance.urlManager.removeFilter(name, value);

      currObjInstance.stateChanged(newUrl, docallback);
      deleted = true;
    }
    return deleted;
  },

  /**
   * Removes all filter and facets
   */
  resetFilters : function() {
    var currObjInstance = this;
    var newUrl =  currObjInstance.urlManager.resetFilters();
    currObjInstance.stateChanged(newUrl,false);
  },

  /**
   * Returns the values for a given facet field
   *
   * @param field the name of the facet
   */
  getFacetValues : function(field) {
    var currObjInstance = this;
    return currObjInstance.urlManager.getFacetValues(field);
  },

  /**
   * Returns the values for a provider facet field
   */
  getProviderIdFacet : function() {
    var currObjInstance = this;
    var providerIDs = currObjInstance.getFacetValues(this.PROVIDER_ID);

    var providerId = null;
    if (providerIDs.length > 0) {
      providerId = providerIDs[0];
    }

    return providerId;
  },

  /**
   * Returns the values for a context facet field
   */
  getContextFacet : function() {
    var currObjInstance = this;
    var contextFacets = currObjInstance.getFacetValues(this.CONTEXT);

    var contextFacet = null;
    if (contextFacets.length > 0) {
      contextFacet = contextFacets[0];
    }

    return contextFacet;
  },

  /**
   * Returns all values of facets
   */
  getAllFacets : function () {
    var currObjInstance = this;
    var facets = currObjInstance.urlManager.getAllFacets();
    return facets ? facets : [];
  },

  /**
   * Persist a given facet value
   *
   * @param field the name of the facet
   * @param value the value of the facet
   */
  setFacet : function(field, value, docallback, doHistory) {
    var currObjInstance = this;
    var written = false;

    if (!currObjInstance.hasFacet(name, value)) {
      var newUrl = currObjInstance.urlManager.setFacet(field,value);
      currObjInstance.stateChanged(newUrl, docallback, doHistory);
      written = true;
    }
    return written;
  },

  /**
   * Removes a given facet value
   *
   * @param field the name of the facet
   * @param value the value of the facet
   */
  removeFacet : function(field, value, docallback, doHistory) {
    var currObjInstance = this;
    var deleted = false;

    if (currObjInstance.hasFacet(field, value)) {
      var newUrl = currObjInstance.urlManager.removeFacet(field,value);
      currObjInstance.stateChanged(newUrl, docallback, doHistory);
      deleted = true;
    }
    return deleted;
  },

  /**
   * Removes all facets
   */
  removeFacets : function(docallback) {
    var currObjInstance = this;
    var newUrl =  currObjInstance.urlManager.removeFacets();
    currObjInstance.stateChanged(newUrl, docallback);
  },

  /**
   * Checks if the stateManer already handles a specific facet value
   *
   * @param field the name of the facet
   * @param value the value of the facet
   */
  hasFacet : function(field, value) {
    var currObjInstance = this;
    var hasFacet = currObjInstance.urlManager.hasFacet(field, value);

    return hasFacet;

  },

  /**
   * Sets the value for the provider_id facet
   *
   * @param value the value of the providerID
   */
  setProviderIdFacet : function (value, docallback, doHistory) {
    var currObjInstance = this;

    var contextFacet = currObjInstance.getContextFacet();
    if(contextFacet) {
      currObjInstance.removeFacet(this.CONTEXT, contextFacet, false);
    }

    //Retrieve existing provider_id facet values
    var oldValue = currObjInstance.getProviderIdFacet();

    if (oldValue) {
      currObjInstance.replaceFacetValue(this.PROVIDER_ID, oldValue, value, docallback, doHistory);
    } else {
      currObjInstance.setFacet(this.PROVIDER_ID, value, docallback);
    }

  },

  /**
   * Sets the value for the context facet
   *
   * @param value the value of the context facet
   */
  setContextFacet : function (value, docallback, doHistory) {
    var currObjInstance = this;

    var providerId = currObjInstance.getProviderIdFacet();
    if(providerId) {
      currObjInstance.removeFacet(this.PROVIDER_ID, providerId, false);
    }

    //Retrieve existing context facet values
    var oldValue = currObjInstance.getContextFacet();
    if (oldValue) {
      currObjInstance.replaceFacetValue(this.CONTEXT, oldValue, value, docallback, doHistory);
    } else {
      currObjInstance.setFacet(this.CONTEXT, value, docallback, doHistory);
    }
  },

  /**
   * Remove the context facet.
   */
  removeContextFacet : function(docallback, doHistory) {
    var currObjInstance = this;
    var contextFacet = currObjInstance.getContextFacet();
    if(contextFacet) {
      currObjInstance.removeFacet(this.CONTEXT, contextFacet, docallback, doHistory);
    }
  },

  /**
   * Remove the provider id facet.
   */
  removeProviderIdFacet : function(docallback, doHistory) {
    var currObjInstance = this;
    var providerIdFacet = currObjInstance.getProviderIdFacet();
    if(providerIdFacet) {
      currObjInstance.removeFacet(this.PROVIDER_ID, providerIdFacet, docallback, doHistory);
    }
  },

  /**
   * Replace the value of a facet with a new value
   */
  replaceFacetValue : function (field, oldValue, newValue, docallback, doHistory) {
    var currObjInstance = this;

    var newUrl = currObjInstance.urlManager.replaceFacetValue(field, oldValue, newValue);
    currObjInstance.stateChanged(newUrl, docallback, doHistory);
  },

  /**
   * Returns the current sort value
   */
  getSort: function() {
    var currObjInstance = this;
    var sort = currObjInstance.urlManager.getParameter('sort');

    return sort;
  },

  /**
   * Sets the sort value
   *
   * @param setValue the value to set for sorting
   */
  setSort: function(setValue, docallback) {
    var currObjInstance = this;
    var newUrl = currObjInstance.urlManager.setParameter('sort', setValue);
    currObjInstance.stateChanged(newUrl, docallback);
  },

  /**
   * Removes the query parameter
   */
  removeQuery : function(docallback) {
    var currObjInstance = this;
    var query = currObjInstance.urlManager.getParameter("query");

    if (query) {
      currObjInstance.stateChanged(currObjInstance.urlManager.removeParameter("query", query), docallback);
    }
  },

  /**
   * Removes the sort parameter
   */
  removeSort : function(docallback) {
    var currObjInstance = this;
    var sort = currObjInstance.getSort();
    if(sort) {
      var newUrl = currObjInstance.urlManager.removeParameter("sort", sort);
      currObjInstance.stateChanged(newUrl, docallback);
    }
  },

  /**
   * Returns the current sort value
   */
  getRows: function() {
    var currObjInstance = this;
    var rows = currObjInstance.urlManager.getParameter('rows');

    return rows ? rows : 20;

  },

  /**
   * Sets the rows value
   *
   * @param setValue the value to set for rows
   */
  setRows: function(setValue, docallback) {
    var currObjInstance = this;
    var newUrl = currObjInstance.urlManager.setParameter('rows', setValue);
    currObjInstance.stateChanged(newUrl, docallback);

  },

  /**
   * Returns the current offset value
   */
  getOffset: function() {
    var currObjInstance = this;
    var offset = currObjInstance.urlManager.getParameter('offset');

    return offset ? offset : 0;

  },

  /**
   * Sets the offset value
   *
   * @param setValue the value to set for offset
   */
  setOffset: function(setValue, docallback) {
    var currObjInstance = this;
    var newUrl = currObjInstance.urlManager.setParameter('offset', setValue);
    currObjInstance.stateChanged(newUrl, docallback);
  },

  /**
   * Returns the current query parameter
   */
  getQuery : function() {
    var currObjInstance = this;
    var query = currObjInstance.urlManager.getParameter('query');

    return query ? query : '';
  },

  /**
   * Persist the query parameter
   *
   * @param setValue the value to set for query
   */
  setQuery : function(setValue, docallback) {
    var currObjInstance = this;
    docallback = docallback || "docallback";
    var newUrl = currObjInstance.urlManager.setParameter('query', setValue);
    currObjInstance.stateChanged(newUrl, docallback);
  },

  /**
   * Returns the current parameters of the url
   */
  getParameters : function() {
    var currObjInstance = this;

    return currObjInstance.urlManager.getParameters();
  },

  /**
   * Sets a list of parameters as new state!
   *
   * @param paramsArray an parameter array
   */
  setParameters : function(paramsArray, docallback) {
    var currObjInstance = this;
    var newUrl = currObjInstance.urlManager.setParameters(paramsArray);
    currObjInstance.stateChanged(newUrl, docallback);
  },

  /**
   * Gets the current url of the urlManager
   */
  getUrl : function() {
    var currObjInstance = this;

    return currObjInstance.urlManager.getUrl();
  },

  /**
   * Adds a history callback function to the StateManager.
   * All interested listener can register here to get informed about history change events.
   */
  addHistoryCallback : function(historyCallback) {
    var currObjInstance = this;

    currObjInstance.historyCallbackListener.push(historyCallback);
  },

  /**
   * Adds a history callback function to the StateManager.
   * All interested listener can register here to get informed about history change events.
   */
  addStateChangeCallback : function(stateChangeCallback) {
    var currObjInstance = this;

    currObjInstance.stateChangeCallbackListener.push(stateChangeCallback);
  },

  /**
   * Pushes a given url to the history stack and sets its value in the urlManager
   */
  pushState: function(url) {
    var currObjInstance = this;
    currObjInstance.stateChanged(url);
  },

  /**
   * Informs all registered listeners that the state has been changed.
   */
  stateChanged : function(url, docallback, doHistory) {
    var currObjInstance = this;

    if (docallback === undefined) {
      docallback = true;
    }

    if (doHistory === undefined) {
      doHistory = true;
    }

    if (url && doHistory) {
      currObjInstance.changeHistory(url);
    }
    //Invoke the callback functions of the controllers. Do not do this if historyChange flag is set
    //We use this variable because in some pages we don't want to update the search result, only the url.
    if (!currObjInstance.historyChange && docallback) {
      $.each( currObjInstance.stateChangeCallbackListener, function(index, func) {
        func();
      });
    }
    currObjInstance.updateUrlButton();
  },

  /**
   * When a filter or a facet is not/selected,
   * update automatically the attribute href the links with class as "update-href-js-button"
   */
  updateUrlButton : function() {
    var currObjInstance = this;
    var parameters = currObjInstance.getParameters();

    $('.update-href-js-button').each(function(){
      var that = this;
      var baseUrl = $(that).attr("href").split('?')[0];
      $(that).attr("href", baseUrl +parameters);
    });

  },

  /**
   * Adds new paths to the history
   *
   * @param path the path to add to the history
   */
  changeHistory : function(path) {
    if (historySupport) {
      window.history.pushState({
        path : path
      }, '', path);
    } else {
      globalUrl = (path.indexOf('?') > -1) ? path.split('?')[1] : path;
      window.location = path;
    }
  }

});
