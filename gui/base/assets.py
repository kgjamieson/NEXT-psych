from flask_assets import Bundle

common_css = Bundle(
    # the old css
    # 'bootstrap-3.3.2-dist/css/bootstrap.min.css',
    # 'css/datatable-bootstrap.min.css',
    # 'css/vendor/helper.css',
    # 'css/content.css',
    # 'css/dashboard.css',
    # 'css/outline.css',

    # the new css
    'css/content.css',
    'startbootstrap-sb-admin-2-1.0.5/bower_components/bootstrap/dist/css/bootstrap.min.css',
    'startbootstrap-sb-admin-2-1.0.5/bower_components/metisMenu/dist/metisMenu.min.css',
    'startbootstrap-sb-admin-2-1.0.5/dist/css/timeline.css',
    'startbootstrap-sb-admin-2-1.0.5/dist/css/sb-admin-2.css',
    'startbootstrap-sb-admin-2-1.0.5/bower_components/morrisjs/morris.css',
    'startbootstrap-sb-admin-2-1.0.5/bower_components/font-awesome/css/font-awesome.min.css',
    filters='cssmin',
    output='public/css/common.css'
)

common_js = Bundle(
    # the old js
    # 'js/vendor/jquery.min.js',
    # 'bootstrap-3.3.2-dist/js/bootstrap.min.js',

    # the new js
    'startbootstrap-sb-admin-2-1.0.5/bower_components/jquery/dist/jquery.min.js',
    'startbootstrap-sb-admin-2-1.0.5/bower_components/bootstrap/dist/js/bootstrap.min.js',
    'startbootstrap-sb-admin-2-1.0.5/bower_components/metisMenu/dist/metisMenu.min.js',
    'startbootstrap-sb-admin-2-1.0.5/bower_components/raphael/raphael-min.js',
    'startbootstrap-sb-admin-2-1.0.5/bower_components/morrisjs/morris.min.js',
    'startbootstrap-sb-admin-2-1.0.5/js/morris-data.js',
    'startbootstrap-sb-admin-2-1.0.5/dist/js/sb-admin-2.js',
    Bundle(
        'js/main.js',
        filters='jsmin'
    ),
    output='public/js/common.js'
)
