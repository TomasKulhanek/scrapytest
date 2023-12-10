const path = require('path');
//const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const DuplicatePackageCheckerPlugin = require('duplicate-package-checker-webpack-plugin');
const project = require('./aurelia_project/aurelia.json');
const { AureliaPlugin } = require('aurelia-webpack-plugin');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');

// config helpers:
const ensureArray = (config) => config && (Array.isArray(config) ? config : [config]) || [];
const when = (condition, config, negativeConfig) =>
  condition ? ensureArray(config) : ensureArray(negativeConfig);

// primary config:
const outDir = path.resolve(__dirname, project.platform.output);
const srcDir = path.resolve(__dirname, 'src');
const nodeModulesDir = path.resolve(__dirname, 'node_modules');
const baseUrl = '';

const cssRules = [
  {
    loader: 'css-loader',
    options: {
      esModule: false
    }
  }
];


module.exports = ({ production } = {}, { extractCss, analyze, hmr, port, host } = {}) => ({
  resolve: {
    extensions: ['.js'],
    modules: [srcDir, 'node_modules'],

    alias: {
      // https://github.com/aurelia/dialog/issues/387
      // Uncomment next line if you had trouble to run aurelia-dialog on IE11
      // 'aurelia-dialog': path.resolve(__dirname, 'node_modules/aurelia-dialog/dist/umd/aurelia-dialog.js'),

      // https://github.com/aurelia/binding/issues/702
      // Enforce single aurelia-binding, to avoid v1/v2 duplication due to
      // out-of-date dependencies on 3rd party aurelia plugins
      'aurelia-binding': path.resolve(__dirname, 'node_modules/aurelia-binding')
    }
  },
  entry: {
    app: [
      // Uncomment next line if you need to support IE11
      // 'promise-polyfill/src/polyfill',
      'aurelia-bootstrapper'
    ]
  },
  mode: production ? 'production' : 'development',
  output: {
    path: outDir,
    publicPath: baseUrl,
    filename: 'scwebcomponents.bundle.js',
    sourceMapFilename: 'scwebcomponents.bundle.map',
    //filename: production ? '[name].[chunkhash].bundle.js' : '[name].[hash].bundle.js',
    //sourceMapFilename: production ? '[name].[chunkhash].bundle.map' : '[name].[hash].bundle.map',
    //chunkFilename: production ? '[name].[chunkhash].chunk.js' : '[name].[hash].chunk.js'

  },
  optimization: {
    runtimeChunk: false,  // separates the runtime chunk, required for long term cacheability
    // moduleIds is the replacement for HashedModuleIdsPlugin and NamedModulesPlugin deprecated in https://github.com/webpack/webpack/releases/tag/v4.16.0
    // changes module id's to use hashes be based on the relative path of the module, required for long term cacheability
    moduleIds: 'deterministic',
    // Use splitChunks to breakdown the App/Aurelia bundle down into smaller chunks
    // https://webpack.js.org/plugins/split-chunks-plugin/
    minimize: production ? true : false,
    minimizer: [new TerserPlugin({
      terserOptions: {
        compress: {
          pure_funcs: [ 'console.log' ],
        },
        mangle: { toplevel: true }
      }
    })],

  },
  performance: { hints: false },
  devServer: {
    // serve index.html for all 404 (required for push-state)
    historyApiFallback: true,
    open: project.platform.open,
    hot: hmr || project.platform.hmr,
    port: port || project.platform.port,
    host: host
  },
  devtool: production ? 'nosources-source-map' : 'cheap-module-source-map',
  module: {
    rules: [
      // CSS required in JS/TS files should use the style-loader that auto-injects it into the website
      // only when the issuer is a .js/.ts file, so the loaders are not applied inside html templates
      {
        test: /\.css$/i,
        issuer: { not: [ /\.html$/i ] },
        use: extractCss ? [{
          loader: MiniCssExtractPlugin.loader
        }, ...cssRules
        ] : ['style-loader', ...cssRules]
      },
      {
        test: /\.css$/i,
        issuer: /\.html$/i,
        // CSS required in templates cannot be extracted safely
        // because Aurelia would try to require it again in runtime
        use: cssRules
      },
      // Skip minimize in production build to avoid complain on unescaped < such as
      // <span>${ c < 5 ? c : 'many' }</span>
      { test: /\.html$/i, loader: 'html-loader', options: { minimize: false } },
      { test: /\.js$/i, loader: 'babel-loader', exclude: nodeModulesDir },
      // embed small images and fonts as Data Urls and larger ones as files:
      //{ test: /\.(png|svg|jpg|jpeg|gif)$/i, type: 'asset' },
      { test: /\.(png|gif|jpg|cur)$/i, loader: 'url-loader', options: { limit: 819200 } },
      //{ test: /\.(woff|woff2|ttf|eot|svg|otf)(\?v=[0-9]\.[0-9]\.[0-9])?$/i,  type:'asset'},
      //{ test: /\.(woff|woff2|ttf|eot|svg|otf)(\?v=[0-9]\.[0-9]\.[0-9])?$/i,  loader: 'url-loader', options: { limit: 8192000 }},
      { test: /\.ttf(\?v=[0-9]\.[0-9]\.[0-9])?$/i, loader: 'url-loader', options: { limit: 8192000000, mimetype: 'font/ttf'  }  },
      { test: /\.eot(\?v=[0-9]\.[0-9]\.[0-9])?$/i, loader: 'url-loader', options: { limit: 8192000000, mimetype: 'application/vnd.ms-fontobject'  }  },
      { test: /\.svg(\?v=[0-9]\.[0-9]\.[0-9])?$/i, loader: 'url-loader', options: { limit: 8192000000, mimetype: 'image/svg+xml'  }  },
      { test: /\.woff2(\?v=[0-9]\.[0-9]\.[0-9])?$/i, loader: 'url-loader', options: {limit: 8192000000, mimetype: 'application/font-woff2' } },
      { test: /\.woff(\?v=[0-9]\.[0-9]\.[0-9])?$/i, loader: 'url-loader', options: {limit: 8192000000, mimetype: 'application/font-woff' } },
      { test: /\.otf(\?v=[0-9]\.[0-9]\.[0-9])?$/i, type: 'asset'},
      // load these fonts normally, as files:
      //{ test: /\.otf(\?v=[0-9]\.[0-9]\.[0-9])?$/i, loader: 'file-loader' },
      { test: /environment\.json$/i, use: [
        {loader: "app-settings-loader", options: {env: production ? 'production' : 'development' }},
      ]}
    ]
  },
  plugins: [
    new DuplicatePackageCheckerPlugin(),
    new AureliaPlugin({
      dist: 'es6',
      aureliaApp: 'scwebcomponents'
    }),
    // ref: https://webpack.js.org/plugins/mini-css-extract-plugin/
    new MiniCssExtractPlugin({ // updated to match the naming conventions for the js files
      filename: production ? '[name].[contenthash].bundle.css' : '[name].[fullhash].bundle.css',
      chunkFilename: production ? '[name].[contenthash].chunk.css' : '[name].[fullhash].chunk.css'
    }),
    new CopyWebpackPlugin({
      patterns: [
        { from: 'static', to: outDir, globOptions: { ignore: ['.*'] } }
      ]
    }),
    ...when(extractCss, new MiniCssExtractPlugin({ // updated to match the naming conventions for the js files
      filename: production ? '[name].[contenthash].bundle.css' : '[name].[hash].bundle.css',
      chunkFilename: production ? '[name].[contenthash].chunk.css' : '[name].[hash].chunk.css'
    })),
    ...when(analyze, new BundleAnalyzerPlugin()),// ignore dot (hidden) files
    /**
     * Note that the usage of following plugin cleans the webpack output directory before build.
     * In case you want to generate any file in the output path as a part of pre-build step, this plugin will likely
     * remove those before the webpack build. In that case consider disabling the plugin, and instead use something like
     * `del` (https://www.npmjs.com/package/del), or `rimraf` (https://www.npmjs.com/package/rimraf).
     */
    new CleanWebpackPlugin()
  ]
});
