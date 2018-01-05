/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
		config.toolbar = [
			{ name: 'document', items: [ 'Print' ] },
			{ name: 'clipboard', items: [ 'Undo', 'Redo' ] },
			// { name: 'styles', items: [ 'Font', 'FontSize' ] },
			{ name: 'basicstyles', items: [ 'Bold', 'Italic', 'RemoveFormat', 'CopyFormatting' ] },
			{ name: 'align', items: [ 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', 'Blockquote' ] },
			{ name: 'links', items: [ 'Link', 'Unlink', 'Superscript', 'Subscript' ] },
			{ name: 'paragraph', items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent' ] },
			{ name: 'tools', items: [ 'Mathjax', 'Scayt',  'Maximize' ] }
		];

		// disallowedContent: 'img{width,height,float}',
		// extraAllowedContent: 'img[width,height,align]',
		// // Enabling extra plugins, available in the full-all preset: http://ckeditor.com/presets-all
		config.extraPlugins = 'mathjax';
		// /*********************** File management support ***********************/
		// // In order to turn on support for file uploads, CKEditor has to be configured to use some server side
		// // solution with file upload/management capabilities, like for example CKFinder.
		// // For more information see http://docs.ckeditor.com/ckeditor4/docs/#!/guide/dev_ckfinder_integration
		// // Uncomment and correct these lines after you setup your local CKFinder instance.
		// // filebrowserBrowseUrl: 'http://example.com/ckfinder/ckfinder.html',
		// // filebrowserUploadUrl: 'http://example.com/ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Files',
		// /*********************** File management support ***********************/
		// // Make the editing area bigger than default.
		// height: 800,
		// // An array of stylesheets to style the WYSIWYG area.
		// // Note: it is recommended to keep your own styles in a separate file in order to make future updates painless.
        config.mathJaxLib = '//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_HTML';
		// contentsCss: [ 'https://cdn.ckeditor.com/4.8.0/full-all/contents.css', 'mystyles.css' ],
		// // This is optional, but will let us define multiple different styles for multiple editors using the same CSS file.
		// bodyClass: 'document-editor',
		// // Reduce the list of block elements listed in the Format dropdown to the most commonly used.
		// format_tags: 'p;h1;h2;h3;pre',
		// // Simplify the Image and Link dialog windows. The "Advanced" tab is not needed in most cases.
		// removeDialogTabs: 'image:advanced;link:advanced',
		// // Define the list of styles which should be available in the Styles dropdown list.
		// // If the "class" attribute is used to style an element, make sure to define the style for the class in "mystyles.css"
		// // (and on your website so that it rendered in the same way).
		// // Note: by default CKEditor looks for styles.js file. Defining stylesSet inline (as below) stops CKEditor from loading
		// // that file, which means one HTTP request less (and a faster startup).
		// // For more information see http://docs.ckeditor.com/ckeditor4/docs/#!/guide/dev_styles
		// stylesSet: [
		// 	/* Inline Styles */
		// 	{ name: 'Marker', element: 'span', attributes: { 'class': 'marker' } },
		// 	{ name: 'Cited Work', element: 'cite' },
		// 	{ name: 'Inline Quotation', element: 'q' },
		// 	/* Object Styles */
		// 	{
		// 		name: 'Special Container',
		// 		element: 'div',
		// 		styles: {
		// 			padding: '5px 10px',
		// 			background: '#eee',
		// 			border: '1px solid #ccc'
		// 		}
		// 	},
		// 	{
		// 		name: 'Compact table',
		// 		element: 'table',
		// 		attributes: {
		// 			cellpadding: '5',
		// 			cellspacing: '0',
		// 			border: '1',
		// 			bordercolor: '#ccc'
		// 		},
		// 		styles: {
		// 			'border-collapse': 'collapse'
		// 		}
		// 	},
		// 	{ name: 'Borderless Table', element: 'table', styles: { 'border-style': 'hidden', 'background-color': '#E6E6FA' } },
		// 	{ name: 'Square Bulleted List', element: 'ul', styles: { 'list-style-type': 'square' } }
		// ]
};
