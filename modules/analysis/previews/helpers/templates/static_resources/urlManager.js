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
 * The state is defined by the selected filter and facet values.
 *
 * The state is stored as query parameters in the browser url
 * To read and manipulate the browser url
 *
 */
de.ddb.apd.search.UrlManager = function() {
  this.init();
};

/**
 * Extend the prototyp of the UrlManager with jQuery
 */
$.extend(de.ddb.apd.search.UrlManager.prototype, {

  /**
   * Initialize the new instance.
   */
  init : function() {
  },

  /**
   * Persist a given filter value
   *
   * @param name the name of the filter
   * @param value the value of the filter
   */
  setFilter : function(name, value) {
    var currObjInstance = this;
    var params = currObjInstance.addNewFilterValueToParams(name + "_" + value);
    var newUrl = $.addParamToCurrentUrl(params);

    return newUrl;
  },

  /**
   * Returns all filter values from the stateManager for a give filter type
   */
  getFilters : function() {
    var filterValuesFromUrl = null;
    filterValuesFromUrl = $.getUrlVar('filterValues');

    return filterValuesFromUrl;
  },

  /**
   * Add a new filter value the current url
   */
  addNewFilterValueToParams : function(filterValue) {
    var currObjInstance = this;
    var paramsFilterValues = currObjInstance.getFilters();

    //The filter values will be stored in a two dimensional Array ["filterValues",['alphabet_A','alphabet_B']]
    var paramsArray = null;

    if (paramsFilterValues) {
      $.each(paramsFilterValues, function(key, value) {
        paramsFilterValues[key] = decodeURIComponent(value.replace(/\+/g, '%20'));
      });
      paramsFilterValues.push(filterValue);
      paramsArray = [ [ 'filterValues', paramsFilterValues ] ];
    } else {
      paramsArray = [ [ 'filterValues', filterValue ] ];
    }

    return paramsArray;
  },

  /**
   * Removes a filter value from the current url
   *
   * @param name the name of the filter
   * @param value the value of the filter
   */
  removeFilter : function(name, value) {
    var filterToRemove = [];

    filterToRemove.push([ 'filterValues', name + "_" + value ]);
    var newUrl = $.removeParamFromUrl(filterToRemove);

    return newUrl;
  },

  /**
   * Removes all filter values from the current url
   */
  resetFilters : function() {
      var toRemove = [];
      var filterValuesFromUrl=$.getUrlVar('filterValues');
      var facetValues = this.getAllFacets();

      if(filterValuesFromUrl) {
        $.each(filterValuesFromUrl, function(key, val) {
          toRemove.push([ 'filterValues', decodeURIComponent(val.replace(/\+/g, '%20')) ]);
        });
      }
      if(facetValues) {
        $.each(facetValues, function(field, value) {
          toRemove.push(['facetValues[]', decodeURIComponent(value.replace(/\+/g, '%20'))]);
        });
      }
      var newUrl = $.removeParamFromUrl(toRemove);
      return newUrl;
  },

  /**
   * Checks if the url already contains a specific filterValue
   *
   * @param name the name of the filter
   * @param value the value of the filter
   */
  hasFilter : function(name, value) {
    var currObjInstance = this;
    var filterValue = name + "_" + value;
    var hasValue = false;
    var paramsFilterValues = currObjInstance.getFilters();

    if (paramsFilterValues) {
      $.each(paramsFilterValues, function(key, val) {
        if (filterValue === decodeURIComponent(val.replace(/\+/g, '%20'))) {
          hasValue = true;
        }
      });
    }

    return hasValue;
  },

  /**
   * Returns the values for a given facet field
   *
   * @param field the name of the facet
   */
  getFacetValues : function(field) {
    var currObjInstance = this;
     var facet = currObjInstance.getAllFacets();
     var values = [];

     if(facet) {
       $.each(facet, function(index, value) {
           var facetField = value.split('%3D')[0];
           if(facetField === field) {
             values.push(value.split('%3D')[1]);
           }
        });
       }

     return values;
  },

  /**
   * Returns all values of facets
   */
  getAllFacets : function () {
    return de.ddb.common.search.getFacetValuesFromUrl();
  },

  /**
   * Replace the value of a facet with a new value
   *
   * @param field the name of the facet
   * @param oldValue the old value of the facet to replace
   * @param newValue the new value of the facet
   */
  replaceFacetValue : function  (field, oldValue, newValue) {
    var currObjInstance = this;

    var oldValueString = field + "%3D" + encodeURIComponent(oldValue);
    var newValueString = field + "%3D" + encodeURIComponent(newValue);

    var newUrl = currObjInstance.getUrl().replace(oldValueString, newValueString);

    return newUrl;
  },


  /**
   * Persist a given facet value
   *
   * @param field the name of the facet
   * @param value the value of the facet
   */
  setFacet : function(field,value) {
    var paramsArray = de.ddb.common.search.addFacetValueToParams(field, value);
    var newUrl = $.addParamToCurrentUrl(paramsArray);

    return newUrl;
  },

  /**
   * Removes a given facet value
   *
   * @param field the name of the facet
   * @param value the value of the facet
   */
  removeFacet : function(field,value) {
    var facetsToRemove = [];
    facetsToRemove.push(['facetValues[]',field + '=' + value]);
    var newUrl = $.removeParamFromUrl(facetsToRemove);

    return newUrl;
  },

  /**
   * Removes all filter values from the current url
   */
  removeFacets : function() {
      var toRemove = [];
      var facetValues = this.getAllFacets();

      if(facetValues) {
        $.each(facetValues, function(field, value) {
          toRemove.push(['facetValues[]', decodeURIComponent(value.replace(/\+/g, '%20'))]);
        });
      }
      var newUrl = $.removeParamFromUrl(toRemove);
      return newUrl;
  },

  /**
   * Checks if the stateManer already handles a specific facet value
   *
   * @param field the name of the facet
   * @param value the value of the facet
   */
  hasFacet : function(field, value) {
    var facetValue = field + "=" + value;
    var hasValue = false;
    var paramsFacetValues = de.ddb.common.search.getFacetValuesFromUrl();

    if (paramsFacetValues) {
      $.each(paramsFacetValues, function(key, val) {
        if (facetValue === decodeURIComponent(val.replace(/\+/g, '%20'))) {
          hasValue = true;
        }
      });
    }

    return hasValue;
  },

  /**
   * Returns the current parameters of the url
   */
  getParameter : function(name) {
    return de.ddb.common.search.getParameterByName(name);
  },

  /**
   * Persist the parameter given
   *
   * @param name the name of the parameter
   * @param value the value to set
   */
  setParameter : function(name, value) {
    var paramsArray = [[name, value]];
    var newUrl = $.addParamToCurrentUrl(paramsArray);

    return newUrl;
  },

  /**
   * Removes a parameter with the given value from the current url
   *
   * @param name the name of the parameter
   * @param name the value of the parameter
   */
  removeParameter : function(name, value) {
    var parameterToRemove = [];

    parameterToRemove.push([ name, value ]);
    var newUrl = $.removeParamFromUrl(parameterToRemove);
    return newUrl;
  },

  /**
   * Sets a list of parameters as new state!
   *
   * @param paramsArray an parameter array
   */
  setParameters : function(paramsArray) {
    var newUrl = $.addParamToCurrentUrl(paramsArray);

    return newUrl;
  },

  /**
   * Returns the current window url
   */
  getUrl : function() {
    return window.location.href;
  },

  /**
   * Returns the current window parameters
   */
  getParameters : function() {
    return window.location.search;
  },

  /**
   * Creates an URL with the given new parameter value and the new base,
   * keeping the other parameters
   *
   * @param url the url that contains the parameters to keep
   * @param parameter the name of the parameter to add/replace
   * @param newParameterValue the value of the parameter to add/replace
   * @param newBaseUrl the new url base
   */
  createURLwithQueryParameter : function (url, parameter, newParameterValue, newBaseUrl) {

    var urlparts= url.split('?');

    if (urlparts.length>=2) {

      var prefix= encodeURIComponent(parameter)+'=';
      var pars= urlparts[1].split(/[&;]/g);

      for (var i= pars.length; i-- > 0;) {
        if (pars[i].lastIndexOf(prefix, 0) !== -1) {
          pars.splice(i, 1);
        }
      }

      if(pars.length>0) {
        newParameterValue = newParameterValue+"&";
      }
      url= newBaseUrl+'?'+parameter+'='+newParameterValue+pars.join('&');
      return url;
    } else {
      url= newBaseUrl+'?'+parameter+'='+newParameterValue;
      return url;
    }
  }
});
