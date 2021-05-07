django.jQuery('select.selectfilter, select.selectfilterstacked').each(function () {
            var $el = $(this),
                data = $el.data();
            SelectFilter.init($el.attr('id'), data.fieldName, parseInt(data.isStacked, 10));
        });