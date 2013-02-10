$(function () {
  function runOverlay($el) {
/// overlay
    // move the overlay div out from ul
    var overlayDiv = $el.find(".image-overlay").detach();
    var parent = $el.parent().parent();
    overlayDiv.appendTo(parent);
    var toOverlay = $($el).find("a[rel]");
//    console.log(toOverlay);
    var close = 'img';
    var expose = {color:'#333', loadSpeed:0, closeSpeed:0, opacity:0.9};
    var overlay = {
      expose:expose,
      close:close,
      onLoad:function () {
        $('.image-overlay img:visible').expose(expose);
      },
      onClose: function() {
        location = '#';
      }
    };
    toOverlay.overlay(overlay).click(function () {
      location = $(this).attr('rel') + '-show';
    });
//    $('body').click(function (e) {
//      location = '#';
//    });


    $('.image-overlay-prev, .image-overlay-next').click(function () {
      var dir = $(this).attr('class').replace('image-overlay-', '');
      var origin = $(this).parent().attr("id");
      var to = $("a[rel=#" + origin + "]").parent()[dir]();
      if (to.length == 0) {
        to = $('.gallery li:' + {prev:'last', next:'first'}[dir]);
      }
      //$(this).parent().find(close).click();
      to.find('a:first').click();
      return false;
    });
    $('body').click(function (e) { /// bind any clinks to element not being ignored and reset the hash
      var ignore = ['image-overlay-thumb', 'image-overlay-full', 'thumbnail'];
      var target = $(e.target);
      if ($.grep(ignore,
        function (name) {
          return target.hasClass(name)
        }).length == 0) { /// reset the hash
        $('.image-overlay img:visible').click();
        location = '#';
      }
    });
    if (location.hash.indexOf('#image-') == 0) { /// handle opening a page already with an hash
      $('a[rel=' + location.hash.replace('-show', '') + ']').click();
      console.log("hash " + location.hash);
    }

  }

  var $container = $('.gallery');
  var $item = '.gallery li';//, .image-overlay';
  $container.imagesLoaded(function () {
    $container.masonry({
      itemSelector:$item,
      isAnimated:true,
      columnWidth:function (containerWidth) {
        return containerWidth / 4;
      }
    });
  });
//    loading:{
//        finishedMsg:'No more items to load.',
//        img:'http://i.imgur.com/6RMhx.gif',
//
//    }
  var itemInject = '.gallery li';
  $container.infinitescroll({
      navSelector:'.pagination', // selector for the paged navigation
      nextSelector:'.next a', // selector for the NEXT link (to page 2)
      itemSelector:itemInject, // selector for all items you'll retrieve
      animate:false,
      extraScrollPx:50,
      bufferPx:30
      //debug        : true
    },
    function (newElements) {
      var $newElems = $(newElements).css({ opacity:0 });
      $newElems.imagesLoaded(function () {
        $newElems.animate({ opacity:1 });
        $container.masonry('appended', $newElems, true);
        runOverlay($newElems);
      });
    }
  );

  runOverlay($(itemInject));
});

