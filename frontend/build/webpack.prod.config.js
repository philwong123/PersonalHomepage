const path = require('path')
const utils = require('./utils')
const webpack = require('webpack')
const config = require('../config')
const merge = require('webpack-merge')
const baseWebpackConfig = require('./webpack.base.config')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const ScriptExtHtmlWebpackPlugin = require('script-ext-html-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin')
const TerserPlugin = require('terser-webpack-plugin')

// For NamedChunksPlugin
const seen = new Set()
const nameLength = 4

const prodWebpackConfig = merge(baseWebpackConfig, {
    mode: 'production',

    output: {
        publicPath: config.build.assetsPublicPath,
        path: config.build.assetsRoot,
        filename: utils.assetsPath('js/[name].[chunkhash:8].js'),
        chunkFilename: utils.assetsPath('js/[name].[chunkhash:8].js')
    },

    module: {
        rules: utils.styleLoaders({
            sourceMap: false,
            extract: true,
            usePostCSS: true
        })
    },

    plugins: [
        new webpack.DefinePlugin({
            'process.env': require('../config/prod.env')
        }),

        new MiniCssExtractPlugin({
            filename: utils.assetsPath('css/[name].[contenthash:8].css'),
            chunkFilename: utils.assetsPath('css/[name].[contenthash:8].css')
        }),

        new HtmlWebpackPlugin({
            filename: config.build.index,
            template: 'src/index.html',
            inject: true,
            templateParameters: {
                BASE_URL: config.build.assetsPublicPath + config.build.assetsSubDirectory,
            },
            minify: {
                removeComments: true,
                collapseWhitespace: true,
                removeAttributeQuotes: true
            }
        }),

        new ScriptExtHtmlWebpackPlugin({
            inline: /runtime\..*\.js$/
        }),

        new webpack.NamedChunksPlugin(chunk => {
            if (chunk.name) {
                return chunk.name
            }
            const modules = Array.from(chunk.modulesIterable)
            if (modules.length > 1) {
                const hash = require('hash-sum')
                const joinedHash = hash(modules.map(m => m.id).join('_'))
                let len = nameLength
                while (seen.has(joinedHash.substr(0, len))) len++
                seen.add(joinedHash.substr(0, len))
                return `chunk-${joinedHash.substr(0, len)}`
            } else {
                return modules[0].id
            }
        }),

        new webpack.HashedModuleIdsPlugin(),
    ],


    optimization: {
        splitChunks: {
            chunks: 'all',
            cacheGroups: {
                libs: {
                    name: 'chunk-libs',
                    test: /[\\/]node_modules[\\/]/,
                    priority: 10,
                    chunks: 'initial'
                },
                elementUI: {
                    name: 'chunk-elementUI',
                    priority: 20,
                    test: /[\\/]node_modules[\\/]element-ui[\\/]/
                }
            }
        },

        runtimeChunk: 'single',

        minimizer: [
            new TerserPlugin({
                terserOptions: {
                    ecma: 8,
                    warnings: false,
                    parse: {},
                    compress: {
                        drop_console: true,
                        drop_debugger: true,
                        pure_funcs: ['console.log'] // 移除console
                    },
                    mangle: {
                        safari10: true
                    }
                },
                sourceMap: false,
                parallel: true,
                cache: true,
                extractComments: false
            }),

            new OptimizeCSSAssetsPlugin()
        ]
    }
});

module.exports = prodWebpackConfig;
