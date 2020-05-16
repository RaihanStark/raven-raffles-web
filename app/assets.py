from flask_assets import Bundle

app_css = Bundle('style.scss', filters='scss', output='styles/app.css')

app_js = Bundle('app.js', filters='jsmin', output='scripts/app.js')

vendor_css = Bundle('vendor/bootstrap.min.css','vendor/all.css', output='styles/vendor.css')

vendor_js = Bundle(
    'vendor/jquery.min.js',
    'vendor/jquery.lazy.min.js',
    'vendor/popper.min.js',
    'vendor/bootstrap.min.js',
    filters='jsmin',
    output='scripts/vendor.js')
