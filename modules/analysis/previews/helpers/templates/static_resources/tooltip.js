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
//tooltip function

$(function() {
  Tooltip = function(element) {
    this.container = element;
    this.init(element);
  };

  $.extend(Tooltip.prototype, {

    hint : null,
    tooltip : null,
    arrow : null,
    opened : false,
    lock : false,
    hoverTime : 0,
    hoverTimeout : 300,
    init : function(element) {
      var currObjInstance = this;
      this.hint = element.attr("data-content");
      this.tooltip = element.siblings("div.tooltip");
      element.removeAttr("title");
      this.tooltip.html(this.hint).text();

      if (this.tooltip.hasClass('hasArrow')) {
        this.arrow = $(document.createElement('div'));
        this.arrow.addClass('arrow');
        this.arrow.appendTo(this.tooltip);
      }

      this.tooltip.hide();
      this.tooltip.removeClass("off");
      element.hover(function() {
        var d = new Date();
        currObjInstance.hoverTime = d.getTime();
        currObjInstance.open();
      });
      this.tooltip.mouseenter(function() {
        currObjInstance.lock = true;
      });
      this.tooltip.mouseleave(function() {
        currObjInstance.close();
      });
      element.mouseleave(function() {
        setTimeout(function() {
          var currentD = new Date();
          if (!currObjInstance.lock
              && currObjInstance.hoverTime + currObjInstance.hoverTimeout - 100 < currentD
                  .getTime()) {
            currObjInstance.close();
          }
        }, currObjInstance.hoverTimeout);
      });
    },
    open : function() {
      var currObjInstance = this;
      if (!this.opened) {
        this.opened = true;
        this.tooltip.fadeIn('fast');

        var positionInfoIcon = currObjInstance.container.offset();

        //set position of arrow under the info icon
        if (this.tooltip.hasClass('hasArrow')) {
          this.arrow.offset({ left: positionInfoIcon.left});
        }
      }
    },
    close : function() {
      this.tooltip.fadeOut('fast');
      this.opened = false;
      this.lock = false;
    }
  });

  $("span.contextual-help").each(function() {
    new Tooltip($(this));
  });
});
