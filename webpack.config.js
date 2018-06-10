const webpack = require('webpack');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    entry: {
        vendor: './src/client/vendor.scss',
        app: './src/client/main'
    },
    resolve: {
        alias: {
            vue: 'vue/dist/vue.esm.js'
        },
        extensions: ['.js', '.vue']
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader'
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                //include: [path.resolve(__dirname, './src/vendor.scss')],
                test: /\.(scss|css)$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader
                    },
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            includePaths: [path.resolve('./node_modules')],
                            sourceMap: true
                        }
                    }
                ]
            }
        ]
    },

    output: {
        filename: '[name].[chunkhash].js',
        path: path.resolve(__dirname, './src/server/static')
    },

    mode: 'production',

    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].[chunkhash].css'
        }),
        new VueLoaderPlugin(),
        new HtmlWebpackPlugin({
            template: path.resolve(__dirname, './src/client', 'index.html'),
            filename: path.resolve(__dirname, './src/server', 'index.html')
        })
    ],

    optimization: {
        splitChunks: {
            chunks: 'async',
            minSize: 30000,
            minChunks: 1,
            name: true,

            cacheGroups: {
                vendors: {
                    test: /[\\/]node_modules[\\/]/,
                    priority: -10
                }
            }
        }
    }
};
