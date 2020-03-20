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
$(document).ready(function() {
    var adElements = $('ul.nav .active-default .dropdown-menu');
    if(adElements.length>0){
        $('ul.nav li').each(function(){
            if(!$(this).hasClass('active-default') && !$(this).parents('li').hasClass('active-default')){
                $(this).mouseover(function(){
                    adElements.each(function(){
                        $(this).css('display','none');
                    });
                });
                $(this).mouseleave(function(){
                    adElements.each(function(){
                        $(this).css('display','');
                    });
                });
            }
        });
    }
});
