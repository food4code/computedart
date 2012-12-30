$(function () {
    var $container = $('.gallery');
    var $item = '.gallery li';
    $container.imagesLoaded(function () {
        $container.masonry({
            itemSelector:$item,
            isAnimated: true,
            columnWidth: function( containerWidth ) {
                return containerWidth / 4;
            }
        });
    });
//    loading:{
//        finishedMsg:'No more items to load.',
//        img:'http://i.imgur.com/6RMhx.gif',
//
//    }

    $container.infinitescroll({
            navSelector:'.pagination', // selector for the paged navigation
            nextSelector:'.next a', // selector for the NEXT link (to page 2)
            itemSelector:$item, // selector for all items you'll retrieve
            animate      : false,
            extraScrollPx: 50,
            bufferPx     : 10
            //debug        : true
        },
        function (newElements) {
            var $newElems = $(newElements).css({ opacity:0 });
            $newElems.imagesLoaded(function () {
                $newElems.animate({ opacity:1 });
                $container.masonry('appended', $newElems, true);
            });
        }
    );

});
