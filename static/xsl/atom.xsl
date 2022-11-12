<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:atom="http://www.w3.org/2005/Atom">
<xsl:template match="atom:feed">
<html>
  <head>
    <title><xsl:value-of select="atom:title"/> (Atom Feed)</title>
    <style type="text/css">
    @import url(/css/rss.css);
    </style>
  </head>
  <body>
    <div id="explanation">
      <h1>Emma Juettner Atom Feed</h1>
      <p>This is an Atom feed, which allows you to read the latest updates from this site.
	  You can use the URL of this page to subscribe to this feed in an RSS reader.
	  I also have an <a href="/feed/rss.xml">RSS feed</a> of the same posts, which you may prefer
	  to use if you don't want to receive the full text of the posts in your RSS reader.</p>
	  <p><a href="/">Return to the main site</a></p>
    </div>
    <div id="content">
      <xsl:for-each select="atom:entry">
	  <hr />
      <div class="article">
        <h2><a href="{id}" rel="bookmark"><xsl:value-of select="atom:title"/></a></h2>
		<p><xsl:value-of select="substring-before(atom:updated, 'T')"/></p>
        <p><xsl:value-of select="atom:summary"/></p>
		<div>
			<details>
			<summary>Full Content</summary>
			<xsl:value-of select="atom:content"/>
			</details>
		</div>
      </div>
      </xsl:for-each>
    </div>
  </body>
</html>
</xsl:template>
</xsl:stylesheet>