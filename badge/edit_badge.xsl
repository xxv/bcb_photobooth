<?xml version='1.0' encoding='utf-8'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:svg="http://www.w3.org/2000/svg"
               xmlns:xlink="http://www.w3.org/1999/xlink"

		version="1.0">

<xsl:output indent="yes" method="xml" 
              omit-xml-declaration="no" encoding="utf-8" />

<xsl:param name="firstname"></xsl:param>
<xsl:param name="lastname"></xsl:param>
<xsl:param name="org"></xsl:param>
<xsl:param name="twitter"></xsl:param>
<xsl:param name="website"></xsl:param>
<xsl:param name="qrcode"></xsl:param>
<xsl:param name="tag1"></xsl:param>
<xsl:param name="tag2"></xsl:param>
<xsl:param name="tag3"></xsl:param>

<!--<xsl:template match="*[@id='qrcode']"><xsl:copy><xsl:apply-templates select="@*"/><xsl:attribute name="xlink:href"><xsl:value-of select="$qrcode"/></xsl:attribute></xsl:copy></xsl:template>-->

<xsl:template match="*[@id='firstname']"><xsl:copy><xsl:apply-templates select="@*"/><xsl:value-of select="$firstname"/></xsl:copy></xsl:template>
<xsl:template match="*[@id='lastname']"><xsl:copy><xsl:apply-templates select="@*"/><xsl:value-of select="$lastname"/></xsl:copy></xsl:template>
<xsl:template match="*[@id='org']"><xsl:copy><xsl:apply-templates select="@*"/><xsl:value-of select="$org"/></xsl:copy></xsl:template>
<xsl:template match="*[@id='twitter_holder']"><xsl:if test="string($twitter)"><xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy></xsl:if></xsl:template>
<xsl:template match="*[@id='twitter']"><xsl:copy><xsl:apply-templates select="@*"/><xsl:value-of select="$twitter"/></xsl:copy></xsl:template>
<xsl:template match="*[@id='website_holder']"><xsl:if test="string($website)"><xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy></xsl:if></xsl:template>
<xsl:template match="*[@id='website']"><xsl:copy><xsl:apply-templates select="@*"/><xsl:value-of select="$website"/></xsl:copy></xsl:template>

<xsl:template match="*[@id='tag1']"><xsl:copy><xsl:apply-templates select="@*"/><xsl:value-of select="$tag1"/></xsl:copy></xsl:template>
<xsl:template match="*[@id='tag2']"><xsl:copy><xsl:apply-templates select="@*"/><xsl:value-of select="$tag2"/></xsl:copy></xsl:template>
<xsl:template match="*[@id='tag3']"><xsl:copy><xsl:apply-templates select="@*"/><xsl:value-of select="$tag3"/></xsl:copy></xsl:template>
<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>
</xsl:stylesheet>
