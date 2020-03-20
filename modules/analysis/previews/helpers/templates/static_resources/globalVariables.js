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
var jsContextPath = "";
var jsLanguage = "";
var jsPageName = "";
var jsInstitutionsListHash = "";
var jsGlossaryUrl="";
var jsGlossaryPageUrl="";
var jsLoggedIn = "";

//apd namespace objects
de = de || {};
de.ddb = de.ddb || {};
de.ddb.apd = de.ddb.apd || {};

$(document).ready(function () {
    var jsVariablesDiv = $('#globalJsVariables');
    var jsPageMeta= $('meta[name=page]').attr("content");
    if (jsVariablesDiv) {
        if (jsVariablesDiv.attr('data-js-context-path')) {
            jsContextPath = jsVariablesDiv.attr('data-js-context-path');
        }
        if (jsVariablesDiv.attr('data-js-language')) {
            jsLanguage = jsVariablesDiv.attr('data-js-language');
        }
        if (jsVariablesDiv.attr('data-js-longitude')) {
          jsLongitude = jsVariablesDiv.attr('data-js-longitude');
        }
        if (jsVariablesDiv.attr('data-js-latitude')) {
          jsLatitude = jsVariablesDiv.attr('data-js-latitude');
        }
        if (jsVariablesDiv.attr('data-js-institutions-list-hash')) {
            jsInstitutionsListHash = jsVariablesDiv.attr('data-js-institutions-list-hash');
        }
        if (jsVariablesDiv.attr('data-js-glossarJsonDbFile')) {
            jsGlossaryUrl = jsVariablesDiv.attr('data-js-glossarJsonDbFile');
        }
        if (jsVariablesDiv.attr('data-js-glossarUrl')) {
            jsGlossaryPageUrl = jsVariablesDiv.attr('data-js-glossarUrl');
        }
        if (jsVariablesDiv.attr('data-js-loggedin')) {
          jsLoggedIn = jsVariablesDiv.attr('data-js-loggedin');
        }
    }
    if (jsPageMeta) {
        jsPageName = jsPageMeta;
    }
});

