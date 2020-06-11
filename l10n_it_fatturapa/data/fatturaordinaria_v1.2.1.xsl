<?xml version="1.0"?>
<xsl:stylesheet 
	version="1.1" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:a="http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2">
	<xsl:output method="html" />

	<xsl:template name="FormatDate">
		<xsl:param name="DateTime" />

		<xsl:variable name="year" select="substring($DateTime,1,4)" />
		<xsl:variable name="month" select="substring($DateTime,6,2)" />
		<xsl:variable name="day" select="substring($DateTime,9,2)" />

		<xsl:value-of select="' ('" />
		<xsl:value-of select="$day" />
		<xsl:value-of select="' '" />
		<xsl:choose>
			<xsl:when test="$month = '1' or $month = '01'">
				Gennaio
			</xsl:when>
			<xsl:when test="$month = '2' or $month = '02'">
				Febbraio
			</xsl:when>
			<xsl:when test="$month = '3' or $month = '03'">
				Marzo
			</xsl:when>
			<xsl:when test="$month = '4' or $month = '04'">
				Aprile
			</xsl:when>
			<xsl:when test="$month = '5' or $month = '05'">
				Maggio
			</xsl:when>
			<xsl:when test="$month = '6' or $month = '06'">
				Giugno
			</xsl:when>
			<xsl:when test="$month = '7' or $month = '07'">
				Luglio
			</xsl:when>
			<xsl:when test="$month = '8' or $month = '08'">
				Agosto
			</xsl:when>
			<xsl:when test="$month = '9' or $month = '09'">
				Settembre
			</xsl:when>
			<xsl:when test="$month = '10'">
				Ottobre
			</xsl:when>
			<xsl:when test="$month = '11'">
				Novembre
			</xsl:when>
			<xsl:when test="$month = '12'">
				Dicembre
			</xsl:when>
			<xsl:otherwise>
				Mese non riconosciuto
			</xsl:otherwise>
		</xsl:choose>
		<xsl:value-of select="' '" />
		<xsl:value-of select="$year" />

		<xsl:variable name="time" select="substring($DateTime,12)" />
		<xsl:if test="$time != ''">
			<xsl:variable name="hh" select="substring($time,1,2)" />
			<xsl:variable name="mm" select="substring($time,4,2)" />
			<xsl:variable name="ss" select="substring($time,7,2)" />

			<xsl:value-of select="' '" />
			<xsl:value-of select="$hh" />
			<xsl:value-of select="':'" />
			<xsl:value-of select="$mm" />
			<xsl:value-of select="':'" />
			<xsl:value-of select="$ss" />
		</xsl:if>
		<xsl:value-of select="')'" />
	</xsl:template>

	<xsl:template match="/">
		<html>
			<head>
				<meta http-equiv="X-UA-Compatible" content="IE=edge" />
				<style type="text/css">
					#fattura-container { width: 100%; position: relative; }

					#fattura-elettronica { font-family: sans-serif; margin-left: auto; margin-right: auto; max-width: 1280px; min-width: 930px; padding: 0; }
					#fattura-elettronica .versione { font-size: 11px; float:right; color: #777777; }
					#fattura-elettronica h1 { padding: 20px 0 0 0; margin: 0; font-size: 30px; }
					#fattura-elettronica h2 { padding: 20px 0 0 0; margin: 0; font-size: 20px; }
					#fattura-elettronica h3 { padding: 20px 0 0 0; margin: 0; font-size: 25px; }
					#fattura-elettronica h4 { padding: 20px 0 0 0; margin: 0; font-size: 20px; }
					#fattura-elettronica h5 { padding: 15px 0 0 0; margin: 0;
					font-size: 17px; font-style: italic; }
					#fattura-elettronica ul { list-style-type: none; margin: 0 !important; padding: 15px 0 0 40px !important; }
					#fattura-elettronica ul li {}
					#fattura-elettronica ul li span { font-weight: bold; }
					#fattura-elettronica div { padding: 0; margin: 0; }

					#fattura-elettronica
					div.page {
					background-color: #fff !important;
					position: relative;

					margin: 20px 0
					50px 0;
					padding: 60px;

					background: -moz-linear-gradient(0% 0 360deg, #FFFFFF, #F2F2F2 20%, #FFFFFF) repeat scroll 0 0 transparent;
					border: 1px solid #CCCCCC;
					-webkitbox-shadow: 0 0 10px rgba(0, 0, 0,
					0.3);
					-mozbox-shadow: 0
					0 10px rgba(0, 0, 0, 0.3);
					box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);

					background: url('logo_sdi_trasparente.jpg') 98% 50px no-repeat;
					}
					#fattura-elettronica div.footer { padding: 50px 0 0 0; margin: 0; font-size: 11px; text-align: center; color: #777777; }
				</style>
			</head>
			<body>
				<div id="fattura-container">
					<!--INIZIO DATI HEADER-->
					<xsl:if test="a:FatturaElettronica">

						<div id="fattura-elettronica">

							<h1>FATTURA ELETTRONICA</h1>

							<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader">
								<div class="page">
									<div class="versione">
										Versione <xsl:value-of select="a:FatturaElettronica/@versione"/>
									</div>

									<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/DatiTrasmissione">
										<!--INIZIO DATI DELLA TRASMISSIONE-->
										<div id="dati-trasmissione">
											<h3>Dati relativi alla trasmissione</h3>
											<ul>
												<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/DatiTrasmissione">

													<xsl:if test="IdTrasmittente">
														<li>
															Identificativo del trasmittente:
															<span>
																<xsl:value-of select="IdTrasmittente/IdPaese" />
																<xsl:value-of select="IdTrasmittente/IdCodice" />
															</span>
														</li>
													</xsl:if>
													<xsl:if test="ProgressivoInvio">
														<li>
															Progressivo di invio:
															<span>
																<xsl:value-of select="ProgressivoInvio" />
															</span>
														</li>
													</xsl:if>
													<xsl:if test="FormatoTrasmissione">
														<li>
															Formato Trasmissione:
															<span>
																<xsl:value-of select="FormatoTrasmissione" />
															</span>
														</li>
													</xsl:if>
													<xsl:if test="CodiceDestinatario">
														<li>
															Codice identificativo destinatario:
															<span>
																<xsl:value-of select="CodiceDestinatario" />
															</span>
														</li>
													</xsl:if>
													<xsl:if test="ContattiTrasmittente/Telefono">
														<li>
															Telefono del trasmittente:
															<span>
																<xsl:value-of select="ContattiTrasmittente/Telefono" />
															</span>
														</li>
													</xsl:if>
													<xsl:if test="ContattiTrasmittente/Email">
														<li>
															E-mail del trasmittente:
															<span>
																<xsl:value-of select="ContattiTrasmittente/Email" />
															</span>
														</li>
													</xsl:if>
													<xsl:if test="PECDestinatario">
														<li>
															Destinatario PEC:
															<span>
																<xsl:value-of select="PECDestinatario" />
															</span>
														</li>
													</xsl:if>
												</xsl:for-each>
											</ul>
										</div>
									</xsl:if>
									<!--FINE DATI DELLA TRASMISSIONE-->

									<!--INIZIO DATI CEDENTE PRESTATORE-->
									<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore">
										<div id="cedente">
											<h3>Dati del cedente / prestatore</h3>

											<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici">
												<h4>Dati anagrafici</h4>

												<ul>
													<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici">
														<xsl:if test="IdFiscaleIVA">
															<li>
																Identificativo fiscale ai fini IVA:
																<span>
																	<xsl:value-of select="IdFiscaleIVA/IdPaese" />
																	<xsl:value-of select="IdFiscaleIVA/IdCodice" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="CodiceFiscale">
															<li>
																Codice fiscale:
																<span>
																	<xsl:value-of select="CodiceFiscale" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Denominazione">
															<li>
																Denominazione:
																<span>
																	<xsl:value-of select="Anagrafica/Denominazione" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Nome">
															<li>
																Nome:
																<span>
																	<xsl:value-of select="Anagrafica/Nome" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Cognome">
															<li>
																Cognome:
																<span>
																	<xsl:value-of select="Anagrafica/Cognome" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Titolo">
															<li>
																Titolo:
																<span>
																	<xsl:value-of select="Anagrafica/Titolo" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/CodEORI">
															<li>
																Codice EORI:
																<span>
																	<xsl:value-of select="Anagrafica/CodEORI" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="AlboProfessionale">
															<li>
																Albo professionale di appartenenza:
																<span>
																	<xsl:value-of select="AlboProfessionale" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="ProvinciaAlbo">
															<li>
																Provincia di competenza dell'Albo:
																<span>
																	<xsl:value-of select="ProvinciaAlbo" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="NumeroIscrizioneAlbo">
															<li>
																Numero iscrizione all'Albo:
																<span>
																	<xsl:value-of select="NumeroIscrizioneAlbo" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DataIscrizioneAlbo">
															<li>
																Data iscrizione all'Albo:
																<span>
																	<xsl:value-of select="DataIscrizioneAlbo" />
																</span>
																<xsl:call-template name="FormatDate">
																	<xsl:with-param name="DateTime" select="DataIscrizioneAlbo" />
																</xsl:call-template>
															</li>
														</xsl:if>
														<xsl:if test="RegimeFiscale">
															<li>
																Regime fiscale:
																<span>
																	<xsl:value-of select="RegimeFiscale" />
																</span>

																<xsl:variable name="RF">
																	<xsl:value-of select="RegimeFiscale" />
																</xsl:variable>
																<xsl:choose>
																	<xsl:when test="$RF='RF01'">
																		(ordinario)
																	</xsl:when>
																	<xsl:when test="$RF='RF02'">
																		(contribuenti minimi)
																	</xsl:when>
																	<xsl:when test="$RF='RF03'">
																		(nuove iniziative produttive) - Non più valido in quanto abrogato dalla legge di stabilità 2015																	
																	</xsl:when>
																	<xsl:when test="$RF='RF04'">
																		(agricoltura e attività connesse e pesca)
																	</xsl:when>
																	<xsl:when test="$RF='RF05'">
																		(vendita sali e tabacchi)
																	</xsl:when>
																	<xsl:when test="$RF='RF06'">
																		(commercio fiammiferi)
																	</xsl:when>
																	<xsl:when test="$RF='RF07'">
																		(editoria)
																	</xsl:when>
																	<xsl:when test="$RF='RF08'">
																		(gestione servizi telefonia pubblica)
																	</xsl:when>
																	<xsl:when test="$RF='RF09'">
																		(rivendita documenti di trasporto pubblico e di sosta)
																	</xsl:when>
																	<xsl:when test="$RF='RF10'">
																		(intrattenimenti, giochi e altre attività di cui alla tariffa allegata al DPR 640/72)
																	</xsl:when>
																	<xsl:when test="$RF='RF11'">
																		(agenzie viaggi e turismo)
																	</xsl:when>
																	<xsl:when test="$RF='RF12'">
																		(agriturismo)
																	</xsl:when>
																	<xsl:when test="$RF='RF13'">
																		(vendite a domicilio)
																	</xsl:when>
																	<xsl:when test="$RF='RF14'">
																		(rivendita beni usati, oggetti d’arte,
																		d’antiquariato o da collezione)
																	</xsl:when>
																	<xsl:when test="$RF='RF15'">
																		(agenzie di vendite all’asta di oggetti d’arte,
																		antiquariato o da collezione)
																	</xsl:when>
																	<xsl:when test="$RF='RF16'">
																		(IVA per cassa P.A.)
																	</xsl:when>
																	<xsl:when test="$RF='RF17'">
																		(IVA per cassa - art. 32-bis, D.L. 83/2012)
																	</xsl:when>
																	<xsl:when test="$RF='RF19'">
																		(Regime forfettario)
																	</xsl:when>
																	<xsl:when test="$RF='RF18'">
																		(altro)
																	</xsl:when>
																	<xsl:when test="$RF=''">
																	</xsl:when>
																	<xsl:otherwise>
																		<span>(!!! codice non previsto !!!)</span>
																	</xsl:otherwise>
																</xsl:choose>
															</li>
														</xsl:if>
													</xsl:for-each>
												</ul>
											</xsl:if>

											<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/Sede">
												<h4>Dati della sede</h4>
												<ul>
													<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/Sede">
														<xsl:if test="Indirizzo">
															<li>
																Indirizzo:
																<span>
																	<xsl:value-of select="Indirizzo" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="NumeroCivico">
															<li>
																Numero civico:
																<span>
																	<xsl:value-of select="NumeroCivico" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="CAP">
															<li>
																CAP:
																<span>
																	<xsl:value-of select="CAP" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Comune">
															<li>
																Comune:
																<span>
																	<xsl:value-of select="Comune" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Provincia">
															<li>
																Provincia:
																<span>
																	<xsl:value-of select="Provincia" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Nazione">
															<li>
																Nazione:
																<span>
																	<xsl:value-of select="Nazione" />
																</span>
															</li>
														</xsl:if>
													</xsl:for-each>
												</ul>
											</xsl:if>

											<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/StabileOrganizzazione">
												<h4>Dati della stabile organizzazione</h4>
												<ul>
													<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/StabileOrganizzazione">
														<xsl:if test="Indirizzo">
															<li>
																Indirizzo:
																<span>
																	<xsl:value-of select="Indirizzo" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="NumeroCivico">
															<li>
																Numero civico:
																<span>
																	<xsl:value-of select="NumeroCivico" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="CAP">
															<li>
																CAP:
																<span>
																	<xsl:value-of select="CAP" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Comune">
															<li>
																Comune:
																<span>
																	<xsl:value-of select="Comune" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Provincia">
															<li>
																Provincia:
																<span>
																	<xsl:value-of select="Provincia" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Nazione">
															<li>
																Nazione:
																<span>
																	<xsl:value-of select="Nazione" />
																</span>
															</li>
														</xsl:if>
													</xsl:for-each>
												</ul>
											</xsl:if>

											<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/IscrizioneREA">
												<h4>Dati di iscrizione nel registro delle imprese</h4>

												<ul>
													<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/IscrizioneREA">
														<xsl:if test="Ufficio">
															<li>
																Provincia Ufficio Registro Imprese:
																<span>
																	<xsl:value-of select="Ufficio" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="NumeroREA">
															<li>
																Numero di iscrizione:
																<span>
																	<xsl:value-of select="NumeroREA" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="CapitaleSociale">
															<li>
																Capitale sociale:
																<span>
																	<xsl:value-of select="CapitaleSociale" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="SocioUnico">
															<li>
																Numero soci:
																<span>
																	<xsl:value-of select="SocioUnico" />
																</span>

																<xsl:variable name="NS">
																	<xsl:value-of select="SocioUnico" />
																</xsl:variable>
																<xsl:choose>
																	<xsl:when test="$NS='SU'">
																		(socio unico)
																	</xsl:when>
																	<xsl:when test="$NS='SM'">
																		(più soci)
																	</xsl:when>
																	<xsl:when test="$NS=''">
																	</xsl:when>
																	<xsl:otherwise>
																		<span>(!!! codice non previsto !!!)</span>
																	</xsl:otherwise>
																</xsl:choose>
															</li>
														</xsl:if>
														<xsl:if test="StatoLiquidazione">
															<li>
																Stato di liquidazione:
																<span>
																	<xsl:value-of select="StatoLiquidazione" />
																</span>

																<xsl:variable name="SL">
																	<xsl:value-of select="StatoLiquidazione" />
																</xsl:variable>
																<xsl:choose>
																	<xsl:when test="$SL='LS'">
																		(in liquidazione)
																	</xsl:when>
																	<xsl:when test="$SL='LN'">
																		(non in liquidazione)
																	</xsl:when>
																	<xsl:when test="$SL=''">
																	</xsl:when>
																	<xsl:otherwise>
																		<span>(!!! codice non previsto !!!)</span>
																	</xsl:otherwise>
																</xsl:choose>
															</li>
														</xsl:if>
													</xsl:for-each>
												</ul>
											</xsl:if>

											<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/Contatti">
												<xsl:if test="Telefono or Fax or Email">
													<h4>Recapiti</h4>
													<ul>
														<xsl:if test="Telefono">
															<li>
																Telefono:
																<span>
																	<xsl:value-of select="Telefono" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Fax">
															<li>
																Fax:
																<span>
																	<xsl:value-of select="Fax" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Email">
															<li>
																E-mail:
																<span>
																	<xsl:value-of select="Email" />
																</span>
															</li>
														</xsl:if>
													</ul>
												</xsl:if>
											</xsl:for-each>

											<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/RiferimentoAmministrazione">
												<h4>Riferimento amministrativo</h4>
												<ul>
													<li>
														Riferimento:
														<span>
															<xsl:value-of select="a:FatturaElettronica/FatturaElettronicaHeader/CedentePrestatore/RiferimentoAmministrazione" />
														</span>
													</li>
												</ul>
											</xsl:if>
										</div>
									</xsl:if>
									<!--FINE DATI CEDENTE PRESTATORE-->

									<!--INIZIO DATI RAPPRESENTANTE FISCALE-->
									<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/RappresentanteFiscale">
										<div id="rappresentante-fiscale">
											<h3>Dati del rappresentante fiscale del cedente / prestatore</h3>

											<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/RappresentanteFiscale/DatiAnagrafici">
												<h4>Dati anagrafici</h4>

												<ul>
													<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/RappresentanteFiscale/DatiAnagrafici">
														<xsl:if test="IdFiscaleIVA">
															<li>
																Identificativo fiscale ai fini IVA:
																<span>
																	<xsl:value-of select="IdFiscaleIVA/IdPaese" />
																	<xsl:value-of select="IdFiscaleIVA/IdCodice" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="CodiceFiscale">
															<li>
																Codice fiscale:
																<span>
																	<xsl:value-of select="CodiceFiscale" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Denominazione">
															<li>
																Denominazione:
																<span>
																	<xsl:value-of select="Anagrafica/Denominazione" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Nome">
															<li>
																Nome:
																<span>
																	<xsl:value-of select="Anagrafica/Nome" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Cognome">
															<li>
																Cognome:
																<span>
																	<xsl:value-of select="Anagrafica/Cognome" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Titolo">
															<li>
																Titolo onorifico:
																<span>
																	<xsl:value-of select="Anagrafica/Titolo" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/CodEORI">
															<li>
																Codice EORI:
																<span>
																	<xsl:value-of select="Anagrafica/CodEORI" />
																</span>
															</li>
														</xsl:if>
													</xsl:for-each>
												</ul>
											</xsl:if>

										</div>
									</xsl:if>
									<!--FINE DATI RAPPRESENTANTE FISCALE-->

									<!--INIZIO DATI CESSIONARIO COMMITTENTE-->
									<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CessionarioCommittente">
										<div id="cessionario">
											<h3>Dati del cessionario / committente</h3>

											<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CessionarioCommittente/DatiAnagrafici">
												<h4>Dati anagrafici</h4>

												<ul>
													<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/CessionarioCommittente/DatiAnagrafici">
														<xsl:if test="IdFiscaleIVA">
															<li>
																Identificativo fiscale ai fini IVA:
																<span>
																	<xsl:value-of select="IdFiscaleIVA/IdPaese" />
																	<xsl:value-of select="IdFiscaleIVA/IdCodice" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="CodiceFiscale">
															<li>
																Codice Fiscale:
																<span>
																	<xsl:value-of select="CodiceFiscale" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Denominazione">
															<li>
																Denominazione:
																<span>
																	<xsl:value-of select="Anagrafica/Denominazione" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Nome">
															<li>
																Nome:
																<span>
																	<xsl:value-of select="Anagrafica/Nome" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Cognome">
															<li>
																Cognome:
																<span>
																	<xsl:value-of select="Anagrafica/Cognome" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/Titolo">
															<li>
																Titolo onorifico:
																<span>
																	<xsl:value-of select="Anagrafica/Titolo" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Anagrafica/CodEORI">
															<li>
																Codice EORI:
																<span>
																	<xsl:value-of select="Anagrafica/CodEORI" />
																</span>
															</li>
														</xsl:if>
													</xsl:for-each>
												</ul>
											</xsl:if>


											<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CessionarioCommittente/Sede">
												<h4>Dati della sede</h4>

												<ul>
													<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/CessionarioCommittente/Sede">
														<xsl:if test="Indirizzo">
															<li>
																Indirizzo:
																<span>
																	<xsl:value-of select="Indirizzo" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="NumeroCivico">
															<li>
																Numero civico:
																<span>
																	<xsl:value-of select="NumeroCivico" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="CAP">
															<li>
																CAP:
																<span>
																	<xsl:value-of select="CAP" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Comune">
															<li>
																Comune:
																<span>
																	<xsl:value-of select="Comune" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Provincia">
															<li>
																Provincia:
																<span>
																	<xsl:value-of select="Provincia" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Nazione">
															<li>
																Nazione:
																<span>
																	<xsl:value-of select="Nazione" />
																</span>
															</li>
														</xsl:if>
													</xsl:for-each>
												</ul>
											</xsl:if>


											<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CessionarioCommittente/StabileOrganizzazione">
												<h4>Stabile organizzazione del cessionario / committente</h4>

												<ul>
													<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/CessionarioCommittente/StabileOrganizzazione">
														<xsl:if test="Indirizzo">
															<li>
																Indirizzo:
																<span>
																	<xsl:value-of select="Indirizzo" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="NumeroCivico">
															<li>
																Numero civico:
																<span>
																	<xsl:value-of select="NumeroCivico" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="CAP">
															<li>
																CAP:
																<span>
																	<xsl:value-of select="CAP" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Comune">
															<li>
																Comune:
																<span>
																	<xsl:value-of select="Comune" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Provincia">
															<li>
																Provincia:
																<span>
																	<xsl:value-of select="Provincia" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="Nazione">
															<li>
																Nazione:
																<span>
																	<xsl:value-of select="Nazione" />
																</span>
															</li>
														</xsl:if>
													</xsl:for-each>
												</ul>
											</xsl:if>
											
											<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/CessionarioCommittente/RappresentanteFiscale">
												<div id="rappresentante-fiscale">
													<h4>Dati del rappresentante fiscale del cessionario / committente</h4>
		
													<ul>
															<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/CessionarioCommittente/RappresentanteFiscale">
																<xsl:if test="IdFiscaleIVA">
																	<li>
																		Identificativo fiscale ai fini IVA:
																		<span>
																			<xsl:value-of select="IdFiscaleIVA/IdPaese" />
																			<xsl:value-of select="IdFiscaleIVA/IdCodice" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="Denominazione">
																	<li>
																		Denominazione:
																		<span>
																			<xsl:value-of select="Denominazione" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="Nome">
																	<li>
																		Nome:
																		<span>
																			<xsl:value-of select="Nome" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="Cognome">
																	<li>
																		Cognome:
																		<span>
																			<xsl:value-of select="Cognome" />
																		</span>
																	</li>
																</xsl:if>
															</xsl:for-each>
														</ul>
												</div>
											</xsl:if>
											<!--FINE DATI RAPPRESENTANTE FISCALE-->
											
										</div>
									</xsl:if>
									<!--FINE DATI CESSIONARIO COMMITTENTE-->

									<!--INIZIO DATI TERZO INTERMEDIARIO SOGGETTO EMITTENTE-->
									<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/TerzoIntermediarioOSoggettoEmittente">
										<div id="terzointermediario">

											<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaHeader/TerzoIntermediarioOSoggettoEmittente">
												<h3>Dati del terzo intermediario soggetto emittente</h3>

												<xsl:if test="DatiAnagrafici">
													<h4>Dati anagrafici</h4>

													<ul>
														<xsl:if test="DatiAnagrafici/IdFiscaleIVA">
															<li>
																Identificativo fiscale ai fini IVA:
																<span>
																	<xsl:value-of select="DatiAnagrafici/IdFiscaleIVA/IdPaese" />
																	<xsl:value-of select="DatiAnagrafici/IdFiscaleIVA/IdCodice" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DatiAnagrafici/CodiceFiscale">
															<li>
																Codice Fiscale:
																<span>
																	<xsl:value-of select="DatiAnagrafici/CodiceFiscale" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DatiAnagrafici/Anagrafica/Denominazione">
															<li>
																Denominazione:
																<span>
																	<xsl:value-of select="DatiAnagrafici/Anagrafica/Denominazione" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DatiAnagrafici/Anagrafica/Nome">
															<li>
																Nome:
																<span>
																	<xsl:value-of select="DatiAnagrafici/Anagrafica/Nome" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DatiAnagrafici/Anagrafica/Cognome">
															<li>
																Cognome:
																<span>
																	<xsl:value-of select="DatiAnagrafici/Anagrafica/Cognome" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DatiAnagrafici/Anagrafica/Titolo">
															<li>
																Titolo onorifico:
																<span>
																	<xsl:value-of select="DatiAnagrafici/Anagrafica/Titolo" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DatiAnagrafici/Anagrafica/CodEORI">
															<li>
																Codice EORI:
																<span>
																	<xsl:value-of select="DatiAnagrafici/Anagrafica/CodEORI" />
																</span>
															</li>
														</xsl:if>
													</ul>
												</xsl:if>
											</xsl:for-each>
										</div>
									</xsl:if>
									<!--FINE DATI TERZO INTERMEDIARIO SOGGETTO EMITTENTE-->

									<!--INIZIO DATI SOGGETTO EMITTENTE-->
									<xsl:if test="a:FatturaElettronica/FatturaElettronicaHeader/SoggettoEmittente">
										<div id="soggetto-emittente">
											<h3>Soggetto emittente la fattura</h3>
											<ul>
												<li>
													Soggetto emittente:
													<span>
														<xsl:value-of select="a:FatturaElettronica/FatturaElettronicaHeader/SoggettoEmittente" />
													</span>
													<xsl:variable name="SC">
														<xsl:value-of select="a:FatturaElettronica/FatturaElettronicaHeader/SoggettoEmittente" />
													</xsl:variable>
													<xsl:choose>
														<xsl:when test="$SC='CC'">
															(cessionario/committente)
														</xsl:when>
														<xsl:when test="$SC='TZ'">
															(terzo)
														</xsl:when>
														<xsl:when test="$SC=''">
														</xsl:when>
														<xsl:otherwise>
															<span>(!!! codice non previsto !!!)</span>
														</xsl:otherwise>
													</xsl:choose>
												</li>
											</ul>
										</div>
									</xsl:if>
									<!--FINE DATI SOGGETTO EMITTENTE-->

									<div class="footer">
										Versione prodotta con foglio di stile SdI
										<a href="http://www.fatturapa.gov.it">www.fatturapa.gov.it</a>
									</div>
								</div>
							</xsl:if>
							<!--FINE DATI HEADER-->

							<!--INIZIO DATI BODY-->

							<xsl:variable name="TOTALBODY">
								<xsl:value-of select="count(a:FatturaElettronica/FatturaElettronicaBody)" />
							</xsl:variable>

							<xsl:for-each select="a:FatturaElettronica/FatturaElettronicaBody">
								<xsl:if test="$TOTALBODY>1">
									<h2>
										Numero documento nel lotto:
										<xsl:value-of select="position()" />
									</h2>
								</xsl:if>

								<div class="page">
									<div class="versione">
										Versione <xsl:value-of select="../@versione"/>
									</div>

									<xsl:if test="DatiGenerali">
										<!--INIZIO DATI GENERALI-->
										<div id="dati-generali">

											<xsl:if test="DatiGenerali/DatiGeneraliDocumento">

												<!--INIZIO DATI GENERALI DOCUMENTO-->
												<div id="dati-generali-documento">
													<h3>Dati generali del documento</h3>

													<ul>
														<xsl:if test="DatiGenerali/DatiGeneraliDocumento/TipoDocumento">
															<li>
																Tipologia documento:
																<span>
																	<xsl:value-of select="DatiGenerali/DatiGeneraliDocumento/TipoDocumento" />
																</span>

																<xsl:variable name="TD">
																	<xsl:value-of select="DatiGenerali/DatiGeneraliDocumento/TipoDocumento" />
																</xsl:variable>
																<xsl:choose>
																	<xsl:when test="$TD='TD01'">
																		(fattura)
																	</xsl:when>
																	<xsl:when test="$TD='TD02'">
																		(acconto/anticipo su fattura)
																	</xsl:when>
																	<xsl:when test="$TD='TD03'">
																		(acconto/anticipo su parcella)
																	</xsl:when>
																	<xsl:when test="$TD='TD04'">
																		(nota di credito)
																	</xsl:when>
																	<xsl:when test="$TD='TD05'">
																		(nota di debito)
																	</xsl:when>
																	<xsl:when test="$TD='TD06'">
																		(parcella)
																	</xsl:when>
																	<xsl:when test="$TD='TD16'">
																		(integrazione fattura 
																		reverse charge interno)
																	</xsl:when>
																	<xsl:when test="$TD='TD17'">
																		(integrazione/autofattura per 
																		acquisto servizi da estero)
																	</xsl:when>
																	<xsl:when test="$TD='TD18'">
																		(integrazione per acquisto 
																		beni intracomunitari)
																	</xsl:when>
																	<xsl:when test="$TD='TD19'">
																		(integrazione/autofattura per 
																		acquisto beni ex art.17 c.2 DPR 633/72)
																	</xsl:when>
																	<xsl:when test="$TD='TD20'">
																		(autofattura per regolarizzazione e 
																		integrazione delle fatture - 
																		art.6 c.8 d.lgs.471/97 o art.46 c.5 D.L.331/93)
																	</xsl:when>
																	<xsl:when test="$TD='TD21'">
																		(autofattura per splafonamento)
																	</xsl:when>
																	<xsl:when test="$TD='TD22'">
																		(estrazione beni da Deposito IVA)
																	</xsl:when>
																	<xsl:when test="$TD='TD23'">
																		(estrazione beni da Deposito IVA 
																		con versamento IVA)
																	</xsl:when>
																	<xsl:when test="$TD='TD24'">
																		(fattura differita - art.21 c.4 lett. a)
																	</xsl:when>
																	<xsl:when test="$TD='TD25'">
																		(fattura differita - art.21 c.4 terzo periodo lett. b)
																	</xsl:when>
																	<xsl:when test="$TD='TD26'">
																		(cessione di beni ammortizzabili e per 
																		passaggi interni - art.36 DPR 633/72)
																	</xsl:when>
																	<xsl:when test="$TD='TD27'">
																		(fattura per autoconsumo o per cessioni 
																		gratuite senza rivalsa)
																	</xsl:when>
																	<xsl:when test="$TD=''">
																	</xsl:when>
																	<xsl:otherwise>
																		<span>(!!! codice non previsto !!!)</span>
																	</xsl:otherwise>
																</xsl:choose>
															</li>
														</xsl:if>
														<xsl:if test="DatiGenerali/DatiGeneraliDocumento/Divisa">
															<li>
																Valuta importi:
																<span>
																	<xsl:value-of select="DatiGenerali/DatiGeneraliDocumento/Divisa" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DatiGenerali/DatiGeneraliDocumento/Data">
															<li>
																Data documento:
																<span>
																	<xsl:value-of select="DatiGenerali/DatiGeneraliDocumento/Data" />
																</span>
																<xsl:call-template name="FormatDate">
																	<xsl:with-param name="DateTime" select="DatiGenerali/DatiGeneraliDocumento/Data" />
																</xsl:call-template>
															</li>
														</xsl:if>
														<xsl:if test="DatiGenerali/DatiGeneraliDocumento/Numero">
															<li>
																Numero documento:
																<span>
																	<xsl:value-of select="DatiGenerali/DatiGeneraliDocumento/Numero" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DatiGenerali/DatiGeneraliDocumento/ImportoTotaleDocumento">
															<li>
																Importo totale documento:
																<span>
																	<xsl:value-of select="DatiGenerali/DatiGeneraliDocumento/ImportoTotaleDocumento" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DatiGenerali/DatiGeneraliDocumento/Arrotondamento">
															<li>
																Arrotondamento su Importo totale documento:
																<span>
																	<xsl:value-of select="DatiGenerali/DatiGeneraliDocumento/Arrotondamento" />
																</span>
															</li>
														</xsl:if>
														<xsl:for-each select="DatiGenerali/DatiGeneraliDocumento/Causale">
															
															<li>
																Causale:
																<span>
																	<xsl:value-of select="current()" />
																</span>
															</li>
															
														</xsl:for-each>
														<xsl:if test="DatiGenerali/DatiGeneraliDocumento/Art73">
															<li>
																Art. 73 DPR 633/72:
																<span>
																	<xsl:value-of select="DatiGenerali/DatiGeneraliDocumento/Art73" />
																</span>
															</li>
														</xsl:if>
													</ul>

													<!--INIZIO DATI DELLA RITENUTA-->
													<xsl:if test="DatiGenerali/DatiGeneraliDocumento/DatiRitenuta">
														<div id="dati-ritenuta">
															<xsl:for-each select="DatiGenerali/DatiGeneraliDocumento/DatiRitenuta">
																<h4>Ritenuta</h4>
																<ul>
																	<xsl:if test="TipoRitenuta">
																		<li>
																			Tipologia ritenuta:
																			<span>
																				<xsl:value-of select="TipoRitenuta" />
																			</span>
																			<xsl:variable name="TR">
																				<xsl:value-of select="TipoRitenuta" />
																			</xsl:variable>
																			<xsl:choose>
																				<xsl:when test="$TR='RT01'">
																					(ritenuta persone fisiche)
																				</xsl:when>
																				<xsl:when test="$TR='RT02'">
																					(ritenuta persone giuridiche)
																				</xsl:when>
																				<xsl:when test="$TR='RT03'">
																					(contributo INPS)
																				</xsl:when>
																				<xsl:when test="$TR='RT04'">
																					(contributo ENASARCO)
																				</xsl:when>
																				<xsl:when test="$TR='RT05'">
																					(contributo ENPAM)
																				</xsl:when>
																				<xsl:when test="$TR='RT06'">
																					(altro contributo previdenziale)
																				</xsl:when>
																				<xsl:when test="$TR=''">
																				</xsl:when>
																				<xsl:otherwise>
																					<span>(!!! codice non previsto !!!)</span>
																				</xsl:otherwise>
																			</xsl:choose>
																		</li>
																	</xsl:if>
																	<xsl:if test="ImportoRitenuta">
																		<li>
																			Importo ritenuta:
																			<span>
																				<xsl:value-of select="ImportoRitenuta" />
																			</span>
																		</li>
																	</xsl:if>
																	<xsl:if test="AliquotaRitenuta">
																		<li>
																			Aliquota ritenuta (%):
																			<span>
																				<xsl:value-of select="AliquotaRitenuta" />
																			</span>
																		</li>
																	</xsl:if>
																	<xsl:if test="CausalePagamento">
																		<li>
																			Causale di pagamento:
																			<span>
																				<xsl:value-of select="CausalePagamento" />
																			</span>
																			<xsl:variable name="CP">
																				<xsl:value-of select="CausalePagamento" />
																			</xsl:variable>
																			<xsl:if test="$CP!=''">
																				(decodifica come da modello CU)
																			</xsl:if>
																		</li>
																	</xsl:if>
																</ul>
															</xsl:for-each>
														</div>
													</xsl:if>
													<!--FINE DATI DELLA RITENUTA-->

													<!--INIZIO DATI DEL BOLLO-->
													<xsl:if test="DatiGenerali/DatiGeneraliDocumento/DatiBollo">
														<div id="dati-bollo">
															<xsl:for-each select="DatiGenerali/DatiGeneraliDocumento/DatiBollo">
																<h4>Bollo</h4>
																<ul>
																	<xsl:if test="BolloVirtuale">
																		<li>
																			Bollo virtuale:
																			<span>
																				<xsl:value-of select="BolloVirtuale" />
																			</span>
																		</li>
																	</xsl:if>
																	<xsl:if test="ImportoBollo">
																		<li>
																			Importo bollo:
																			<span>
																				<xsl:value-of select="ImportoBollo" />
																			</span>
																		</li>
																	</xsl:if>
																</ul>
															</xsl:for-each>
														</div>
													</xsl:if>
													<!--FINE DATI DEL BOLLO-->

													<!--INIZIO DATI DELLA CASSA PREVIDENZIALE-->
													<xsl:if test="DatiGenerali/DatiGeneraliDocumento/DatiCassaPrevidenziale">
														<div id="dati-cassa-previdenziale">
															<h4>Cassa previdenziale</h4>
															<xsl:for-each select="DatiGenerali/DatiGeneraliDocumento/DatiCassaPrevidenziale">
																<ul>
																	<xsl:if test="TipoCassa">
																		<li>
																			Tipologia cassa previdenziale:
																			<span>
																				<xsl:value-of select="TipoCassa" />
																			</span>
																			<xsl:variable name="TC">
																				<xsl:value-of select="TipoCassa" />
																			</xsl:variable>
																			<xsl:choose>
																				<xsl:when test="$TC='TC01'">
																					(Cassa Nazionale Previdenza e Assistenza Avvocati
																					e Procuratori legali)
																				</xsl:when>
																				<xsl:when test="$TC='TC02'">
																					(Cassa Previdenza Dottori Commercialisti)
																				</xsl:when>
																				<xsl:when test="$TC='TC03'">
																					(Cassa Previdenza e Assistenza Geometri)
																				</xsl:when>
																				<xsl:when test="$TC='TC04'">
																					(Cassa Nazionale Previdenza e Assistenza
																					Ingegneri e Architetti liberi profess.)
																				</xsl:when>
																				<xsl:when test="$TC='TC05'">
																					(Cassa Nazionale del Notariato)
																				</xsl:when>
																				<xsl:when test="$TC='TC06'">
																					(Cassa Nazionale Previdenza e Assistenza
																					Ragionieri e Periti commerciali)
																				</xsl:when>
																				<xsl:when test="$TC='TC07'">
																					(Ente Nazionale Assistenza Agenti e Rappresentanti
																					di Commercio-ENASARCO)
																				</xsl:when>
																				<xsl:when test="$TC='TC08'">
																					(Ente Nazionale Previdenza e Assistenza Consulenti
																					del Lavoro-ENPACL)
																				</xsl:when>
																				<xsl:when test="$TC='TC09'">
																					(Ente Nazionale Previdenza e Assistenza
																					Medici-ENPAM)
																				</xsl:when>
																				<xsl:when test="$TC='TC10'">
																					(Ente Nazionale Previdenza e Assistenza
																					Farmacisti-ENPAF)
																				</xsl:when>
																				<xsl:when test="$TC='TC11'">
																					(Ente Nazionale Previdenza e Assistenza
																					Veterinari-ENPAV)
																				</xsl:when>
																				<xsl:when test="$TC='TC12'">
																					(Ente Nazionale Previdenza e Assistenza Impiegati
																					dell'Agricoltura-ENPAIA)
																				</xsl:when>
																				<xsl:when test="$TC='TC13'">
																					(Fondo Previdenza Impiegati Imprese di Spedizione
																					e Agenzie Marittime)
																				</xsl:when>
																				<xsl:when test="$TC='TC14'">
																					(Istituto Nazionale Previdenza Giornalisti
																					Italiani-INPGI)
																				</xsl:when>
																				<xsl:when test="$TC='TC15'">
																					(Opera Nazionale Assistenza Orfani Sanitari
																					Italiani-ONAOSI)
																				</xsl:when>
																				<xsl:when test="$TC='TC16'">
																					(Cassa Autonoma Assistenza Integrativa
																					Giornalisti Italiani-CASAGIT)
																				</xsl:when>
																				<xsl:when test="$TC='TC17'">
																					(Ente Previdenza Periti Industriali e Periti
																					Industriali Laureati-EPPI)
																				</xsl:when>
																				<xsl:when test="$TC='TC18'">
																					(Ente Previdenza e Assistenza
																					Pluricategoriale-EPAP)
																				</xsl:when>
																				<xsl:when test="$TC='TC19'">
																					(Ente Nazionale Previdenza e Assistenza
																					Biologi-ENPAB)
																				</xsl:when>
																				<xsl:when test="$TC='TC20'">
																					(Ente Nazionale Previdenza e Assistenza
																					Professione Infermieristica-ENPAPI)
																				</xsl:when>
																				<xsl:when test="$TC='TC21'">
																					(Ente Nazionale Previdenza e Assistenza
																					Psicologi-ENPAP)
																				</xsl:when>
																				<xsl:when test="$TC='TC22'">
																					(INPS)
																				</xsl:when>
																				<xsl:when test="$TC=''">
																				</xsl:when>
																				<xsl:otherwise>
																					<span>(!!! codice non previsto !!!)</span>
																				</xsl:otherwise>
																			</xsl:choose>
																		</li>
																	</xsl:if>
																	<xsl:if test="AlCassa">
																		<li>
																			Aliquota contributo cassa (%):
																			<span>
																				<xsl:value-of select="AlCassa" />
																			</span>
																		</li>
																	</xsl:if>
																	<xsl:if test="ImportoContributoCassa">
																		<li>
																			Importo contributo cassa:
																			<span>
																				<xsl:value-of select="ImportoContributoCassa" />
																			</span>
																		</li>
																	</xsl:if>
																	<xsl:if test="ImponibileCassa">
																		<li>
																			Imponibile previdenziale:
																			<span>
																				<xsl:value-of select="ImponibileCassa" />
																			</span>
																		</li>
																	</xsl:if>
																	<xsl:if test="AliquotaIVA">
																		<li>
																			Aliquota IVA applicata:
																			<span>
																				<xsl:value-of select="AliquotaIVA" />
																			</span>
																		</li>
																	</xsl:if>
																	<xsl:if test="Ritenuta">
																		<li>
																			Contributo cassa soggetto a ritenuta:
																			<span>
																				<xsl:value-of select="Ritenuta" />
																			</span>
																		</li>
																	</xsl:if>
																	<xsl:if test="Natura">
																		<li>
																			Tipologia di non imponibilità del contributo:
																			<span>
																				<xsl:value-of select="Natura" />
																			</span>
																			<xsl:variable name="NT">
																				<xsl:value-of select="Natura" />
																			</xsl:variable>
																			<xsl:choose>
																				<xsl:when test="$NT='N1'">
																					(escluse ex art. 15)
																				</xsl:when>
																				<xsl:when test="$NT='N2'">
																					(non soggette)
																				</xsl:when>
																				<xsl:when test="$NT='N2.1'">
																					(non soggette ad IVA - artt. da 7 a 7-septies 
																					del DPR 633/72)
																				</xsl:when>
																				<xsl:when test="$NT='N2.2'">
																					(non soggette - altri casi)
																				</xsl:when>
																				<xsl:when test="$NT='N3'">
																					(non imponibili)
																				</xsl:when>
																				<xsl:when test="$NT='N3.1'">
																					(non imponibili - esportazioni)
																				</xsl:when>
																				<xsl:when test="$NT='N3.2'">
																					(non imponibili - cessioni intracomunitarie)
																				</xsl:when>
																				<xsl:when test="$NT='N3.3'">
																					(non imponibili - cessioni verso S.Marino)
																				</xsl:when>
																				<xsl:when test="$NT='N3.4'">
																					(non imponibili - operazioni assimilate alle 
																					cessioni all'esportazione)
																				</xsl:when>
																				<xsl:when test="$NT='N3.5'">
																					(non imponibili - a seguito di dichiarazioni 
																					d'intento)
																				</xsl:when>
																				<xsl:when test="$NT='N3.6'">
																					(non imponibili - altre operazioni che non 
																					concorrono alla formazione del plafond)
																				</xsl:when>
																				<xsl:when test="$NT='N4'">
																					(esenti)
																				</xsl:when>
																				<xsl:when test="$NT='N5'">
																					(regime del margine / IVA non esposta in fattura)
																				</xsl:when>
																				<xsl:when test="$NT='N6'">
																					(inversione contabile per le operazioni in reverse 
																					charge ovvero nei casi di autofatturazione per 
																					acquisti extra UE di servizi ovvero per importazioni 
																					di beni nei soli casi previsti)
																				</xsl:when>
																				<xsl:when test="$NT='N6.1'">
																					(inversione contabile - cessione di rottami e 
																					altri materiali di recupero)
																				</xsl:when>
																				<xsl:when test="$NT='N6.2'">
																					(inversione contabile - cessione di oro e 
																					argento puro)
																				</xsl:when>
																				<xsl:when test="$NT='N6.3'">
																					(inversione contabile - subappalto nel settore 
																					edile)
																				</xsl:when>
																				<xsl:when test="$NT='N6.4'">
																					(inversione contabile - cessione di fabbricati)
																				</xsl:when>
																				<xsl:when test="$NT='N6.5'">
																					(inversione contabile - cessione di telefoni 
																					cellulari)
																				</xsl:when>
																				<xsl:when test="$NT='N6.6'">
																					(inversione contabile - cessione di prodotti 
																					elettronici)
																				</xsl:when>
																				<xsl:when test="$NT='N6.7'">
																					(inversione contabile - prestazioni comparto 
																					edile e settori connessi)
																				</xsl:when>
																				<xsl:when test="$NT='N6.8'">
																					(inversione contabile - operazioni settore 
																					energetico)
																				</xsl:when>
																				<xsl:when test="$NT='N6.9'">
																					(inversione contabile - altri casi)
																				</xsl:when>
																				<xsl:when test="$NT='N7'">
																					(IVA assolta in altro stato UE - vendite a distanza 
																					ex art.40 c.3 e 4 e art.41 c.1 lett. b DL 331/93; 
																					prestazione di servizi di telecomunicazioni, 
																					tele-radiodiffusione ed elettronici ex art.7-sexies 
																					lett. f, g, e art.74-sexies DPR 633/72)
																				</xsl:when>
																				<xsl:when test="$NT=''">
																				</xsl:when>
																				<xsl:otherwise>
																					<span>(!!! codice non previsto !!!)</span>
																				</xsl:otherwise>
																			</xsl:choose>
																		</li>
																	</xsl:if>
																	<xsl:if test="RiferimentoAmministrazione">
																		<li>
																			Riferimento amministrativo / contabile:
																			<span>
																				<xsl:value-of select="RiferimentoAmministrazione" />
																			</span>
																		</li>
																	</xsl:if>
																</ul>
															</xsl:for-each>
														</div>
													</xsl:if>
													<!--FINE DATI DELLA CASSA PREVIDENZIALE-->

													<!--INIZIO DATI SCONTO / MAGGIORAZIONE-->
													<xsl:if test="DatiGenerali/DatiGeneraliDocumento/ScontoMaggiorazione">
														<h4>Sconto/maggiorazione</h4>
														<div id="dati-sconto-maggiorazione">
															<xsl:for-each select="DatiGenerali/DatiGeneraliDocumento/ScontoMaggiorazione">
																<ul>
																	<xsl:if test="Tipo">
																		<li>
																			Tipologia:
																			<span>
																				<xsl:value-of select="Tipo" />
																			</span>
																			<xsl:variable name="TSM">
																				<xsl:value-of select="Tipo" />
																			</xsl:variable>
																			<xsl:choose>
																				<xsl:when test="$TSM='SC'">

																					(sconto)
																				</xsl:when>
																				<xsl:when test="$TSM='MG'">

																					(maggiorazione)
																				</xsl:when>
																				<xsl:otherwise>

																					<span>(!!! codice non previsto !!!)</span>
																				</xsl:otherwise>
																			</xsl:choose>
																		</li>
																	</xsl:if>
																	<xsl:if test="Percentuale">
																		<li>
																			Percentuale:
																			<span>
																				<xsl:value-of select="Percentuale" />
																			</span>
																		</li>
																	</xsl:if>
																	<xsl:if test="Importo">
																		<li>
																			Importo:
																			<span>
																				<xsl:value-of select="Importo" />
																			</span>
																		</li>
																	</xsl:if>
																</ul>
															</xsl:for-each>
														</div>
													</xsl:if>
													<!--FINE DATI SCONTO / MAGGIORAZIONE-->

												</div>
											</xsl:if>
											<!--FINE DATI GENERALI DOCUMENTO-->

											<!--INIZIO DATI DELL'ORDINE DI ACQUISTO-->
											<xsl:if test="DatiGenerali/DatiOrdineAcquisto">
												<div id="dati-ordine-acquisto">
													<h3>Dati dell'ordine di acquisto</h3>

													<xsl:for-each select="DatiGenerali/DatiOrdineAcquisto">
														<ul>
															<xsl:if test="RiferimentoNumeroLinea">
																<li>
																	Numero linea di fattura a cui si riferisce:
																	<xsl:for-each select="RiferimentoNumeroLinea">
																		<span>
																			<xsl:if test="(position( )) > 1">
																				,
																			</xsl:if>
																			<xsl:value-of select="." />
																		</span>
																	</xsl:for-each>
																</li>
															</xsl:if>
															<xsl:if test="IdDocumento">
																<li>
																	Identificativo ordine di acquisto:
																	<span>
																		<xsl:value-of select="IdDocumento" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Data">
																<li>
																	Data ordine di acquisto:
																	<span>
																		<xsl:value-of select="Data" />
																	</span>
																	<xsl:call-template name="FormatDate">
																		<xsl:with-param name="DateTime" select="Data" />
																	</xsl:call-template>
																</li>
															</xsl:if>
															<xsl:if test="NumItem">
																<li>
																	Numero linea ordine di acquisto:
																	<span>
																		<xsl:value-of select="NumItem" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCommessaConvenzione">
																<li>
																	Codice commessa/convenzione:
																	<span>
																		<xsl:value-of select="CodiceCommessaConvenzione" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCUP">
																<li>
																	Codice Unitario Progetto (CUP):
																	<span>
																		<xsl:value-of select="CodiceCUP" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCIG">
																<li>
																	Codice Identificativo Gara (CIG):
																	<span>
																		<xsl:value-of select="CodiceCIG" />
																	</span>
																</li>
															</xsl:if>
														</ul>
													</xsl:for-each>
												</div>
											</xsl:if>
											<!--FINE DATI DELL'ORDINE DI ACQUISTO-->

											<!--INIZIO DATI DEL CONTRATTO-->
											<xsl:if test="DatiGenerali/DatiContratto">
												<div id="dati-contratto">
													<h3>Dati del contratto</h3>
													<xsl:for-each select="DatiGenerali/DatiContratto">
														<ul>
															<xsl:if test="RiferimentoNumeroLinea">
																<li>
																	Numero linea di fattura a cui si riferisce:
																	<xsl:for-each select="RiferimentoNumeroLinea">
																		<span>
																			<xsl:if test="(position( )) > 1">
																				,
																			</xsl:if>
																			<xsl:value-of select="." />
																		</span>
																	</xsl:for-each>
																</li>
															</xsl:if>
															<xsl:if test="IdDocumento">
																<li>
																	Identificativo contratto:
																	<span>
																		<xsl:value-of select="IdDocumento" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Data">
																<li>
																	Data contratto:
																	<span>
																		<xsl:value-of select="Data" />
																	</span>
																	<xsl:call-template name="FormatDate">
																		<xsl:with-param name="DateTime" select="Data" />
																	</xsl:call-template>
																</li>
															</xsl:if>
															<xsl:if test="NumItem">
																<li>
																	Numero linea contratto:
																	<span>
																		<xsl:value-of select="NumItem" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCommessaConvenzione">
																<li>
																	Codice commessa/convenzione:
																	<span>
																		<xsl:value-of select="CodiceCommessaConvenzione" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCUP">
																<li>
																	Codice Unitario Progetto (CUP):
																	<span>
																		<xsl:value-of select="CodiceCUP" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCIG">
																<li>
																	Codice Identificativo Gara (CIG):
																	<span>
																		<xsl:value-of select="CodiceCIG" />
																	</span>
																</li>
															</xsl:if>
														</ul>
													</xsl:for-each>
												</div>
											</xsl:if>
											<!--FINE DATI DEL CONTRATTO-->

											<!--INIZIO DATI CONVENZIONE-->
											<xsl:if test="DatiGenerali/DatiConvenzione">
												<div id="dati-convenzione">
													<h3>Dati della convenzione</h3>
													<xsl:for-each select="DatiGenerali/DatiConvenzione">
														<ul>
															<xsl:if test="RiferimentoNumeroLinea">
																<li>
																	Numero linea di fattura a cui si riferisce:
																	<xsl:for-each select="RiferimentoNumeroLinea">
																		<span>
																			<xsl:if test="(position( )) > 1">
																				,
																			</xsl:if>
																			<xsl:value-of select="." />
																		</span>

																	</xsl:for-each>
																</li>
															</xsl:if>
															<xsl:if test="IdDocumento">
																<li>
																	Identificativo convenzione:
																	<span>
																		<xsl:value-of select="IdDocumento" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Data">
																<li>
																	Data convenzione:
																	<span>
																		<xsl:value-of select="Data" />
																	</span>
																	<xsl:call-template name="FormatDate">
																		<xsl:with-param name="DateTime" select="Data" />
																	</xsl:call-template>
																</li>
															</xsl:if>
															<xsl:if test="NumItem">
																<li>
																	Numero linea convenzione:
																	<span>
																		<xsl:value-of select="NumItem" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCommessaConvenzione">
																<li>
																	Codice commessa/convenzione:
																	<span>
																		<xsl:value-of select="CodiceCommessaConvenzione" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCUP">
																<li>
																	Codice Unitario Progetto (CUP):
																	<span>
																		<xsl:value-of select="CodiceCUP" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCIG">
																<li>
																	Codice Identificativo Gara (CIG):
																	<span>
																		<xsl:value-of select="CodiceCIG" />
																	</span>
																</li>
															</xsl:if>
														</ul>
													</xsl:for-each>
												</div>
											</xsl:if>
											<!--FINE DATI CONVENZIONE-->

											<!--INIZIO DATI RICEZIONE-->
											<xsl:if test="DatiGenerali/DatiRicezione">
												<div id="dati-ricezione">
													<h3>Dati della ricezione</h3>
													<xsl:for-each select="DatiGenerali/DatiRicezione">
														<ul>
															<xsl:if test="RiferimentoNumeroLinea">
																<li>
																	Numero linea di fattura a cui si riferisce:
																	<xsl:for-each select="RiferimentoNumeroLinea">
																		<span>
																			<xsl:if test="(position( )) > 1">
																				,
																			</xsl:if>
																			<xsl:value-of select="." />
																		</span>

																	</xsl:for-each>
																</li>
															</xsl:if>
															<xsl:if test="IdDocumento">
																<li>
																	Identificativo ricezione:
																	<span>
																		<xsl:value-of select="IdDocumento" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Data">
																<li>
																	Data ricezione:
																	<span>
																		<xsl:value-of select="Data" />
																	</span>
																	<xsl:call-template name="FormatDate">
																		<xsl:with-param name="DateTime" select="Data" />
																	</xsl:call-template>
																</li>
															</xsl:if>
															<xsl:if test="NumItem">
																<li>
																	Numero linea ricezione:
																	<span>
																		<xsl:value-of select="NumItem" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCommessaConvenzione">
																<li>
																	Codice commessa/convenzione:
																	<span>
																		<xsl:value-of select="CodiceCommessaConvenzione" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCUP">
																<li>
																	Codice Unitario Progetto (CUP):
																	<span>
																		<xsl:value-of select="CodiceCUP" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCIG">
																<li>
																	Codice Identificativo Gara (CIG):
																	<span>
																		<xsl:value-of select="CodiceCIG" />
																	</span>
																</li>
															</xsl:if>
														</ul>
													</xsl:for-each>
												</div>
											</xsl:if>
											<!--FINE DATI RICEZIONE-->

											<!--INIZIO DATI FATTURE COLLEGATE-->
											<xsl:if test="DatiGenerali/DatiFattureCollegate">
												<div id="dati-fatture-collegate">
													<h3>Dati della fattura collegata</h3>
													<xsl:for-each select="DatiGenerali/DatiFattureCollegate">
														<ul>
															<xsl:if test="RiferimentoNumeroLinea">
																<li>
																	Numero linea di fattura a cui si riferisce:
																	<xsl:for-each select="RiferimentoNumeroLinea">
																		<span>
																			<xsl:if test="(position( )) > 1">
																				,
																			</xsl:if>
																			<xsl:value-of select="." />
																		</span>

																	</xsl:for-each>
																</li>
															</xsl:if>
															<xsl:if test="IdDocumento">
																<li>
																	Identificativo fattura collegata:
																	<span>
																		<xsl:value-of select="IdDocumento" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Data">
																<li>
																	Data fattura collegata:
																	<span>
																		<xsl:value-of select="Data" />
																	</span>
																	<xsl:call-template name="FormatDate">
																		<xsl:with-param name="DateTime" select="Data" />
																	</xsl:call-template>
																</li>
															</xsl:if>
															<xsl:if test="NumItem">
																<li>
																	Numero linea fattura collegata:
																	<span>
																		<xsl:value-of select="NumItem" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCommessaConvenzione">
																<li>
																	Codice commessa/convenzione:
																	<span>
																		<xsl:value-of select="CodiceCommessaConvenzione" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCUP">
																<li>
																	Codice Unitario Progetto (CUP):
																	<span>
																		<xsl:value-of select="CodiceCUP" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="CodiceCIG">
																<li>
																	Codice Identificativo Gara (CIG):
																	<span>
																		<xsl:value-of select="CodiceCIG" />
																	</span>
																</li>
															</xsl:if>
														</ul>
													</xsl:for-each>
												</div>
											</xsl:if>
											<!--FINE DATI FATTURE COLLEGATE-->

											<!--INIZIO DATI RIFERIMENTO SAL-->
											<xsl:if test="DatiGenerali/DatiSAL">
												<div id="dati-sal">
													<h3>Stato avanzamento lavori</h3>
													<ul>
														<xsl:if test="DatiGenerali/DatiSAL/RiferimentoFase">
															<li>
																Numero fase avanzamento:
																<xsl:for-each select="DatiGenerali/DatiSAL/RiferimentoFase">
																	<span>
																		<xsl:if test="(position( )) > 1">
																			,
																		</xsl:if>
																		<xsl:value-of select="." />
																	</span>
																</xsl:for-each>
															</li>
														</xsl:if>
													</ul>
												</div>
											</xsl:if>
											<!--FINE DATI RIFERIMENTO SAL-->

											<!--INIZIO DATI  DDT-->
											<xsl:if test="DatiGenerali/DatiDDT">
												<div id="dati-ddt">
													<h3>Dati del documento di trasporto</h3>
													<xsl:for-each select="DatiGenerali/DatiDDT">
														<ul>
															<xsl:if test="NumeroDDT">
																<li>
																	Numero DDT:
																	<span>
																		<xsl:value-of select="NumeroDDT" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="DataDDT">
																<li>
																	Data DDT:
																	<span>
																		<xsl:value-of select="DataDDT" />
																	</span>
																	<xsl:call-template name="FormatDate">
																		<xsl:with-param name="DateTime" select="DataDDT" />
																	</xsl:call-template>
																</li>
															</xsl:if>
															<xsl:if test="RiferimentoNumeroLinea">
																<li>
																	Numero linea di fattura a cui si riferisce:
																	<xsl:for-each select="RiferimentoNumeroLinea">
																		<span>
																			<xsl:if test="(position( )) > 1">
																				,
																			</xsl:if>
																			<xsl:value-of select="." />
																		</span>
																	</xsl:for-each>
																</li>
															</xsl:if>
														</ul>
													</xsl:for-each>
												</div>
											</xsl:if>
											<!--FINE DATI DDT-->

											<!--INIZIO DATI  TRASPORTO-->
											<xsl:if test="DatiGenerali/DatiTrasporto">
												<div id="dati-trasporto">
													<h3>Dati relativi al trasporto</h3>

													<xsl:if test="DatiGenerali/DatiTrasporto/DatiAnagraficiVettore">
														<h4>Dati del vettore</h4>

														<ul>
															<xsl:for-each select="DatiGenerali/DatiTrasporto/DatiAnagraficiVettore">
																<xsl:if test="IdFiscaleIVA/IdPaese">
																	<li>
																		Identificativo fiscale ai fini IVA:
																		<span>
																			<xsl:value-of select="IdFiscaleIVA/IdPaese" />
																			<xsl:value-of select="IdFiscaleIVA/IdCodice" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="CodiceFiscale">
																	<li>
																		Codice Fiscale:
																		<span>
																			<xsl:value-of select="CodiceFiscale" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="Anagrafica/Denominazione">
																	<li>
																		Denominazione:
																		<span>
																			<xsl:value-of select="Anagrafica/Denominazione" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="Anagrafica/Nome">
																	<li>
																		Nome:
																		<span>
																			<xsl:value-of select="Anagrafica/Nome" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="Anagrafica/Cognome">
																	<li>
																		Cognome:
																		<span>
																			<xsl:value-of select="Anagrafica/Cognome" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="Anagrafica/Titolo">
																	<li>
																		Titolo onorifico:
																		<span>
																			<xsl:value-of select="Anagrafica/Titolo" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="Anagrafica/CodEORI">
																	<li>
																		Codice EORI:
																		<span>
																			<xsl:value-of select="Anagrafica/CodEORI" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="NumeroLicenzaGuida">
																	<li>
																		Numero licenza di guida:
																		<span>
																			<xsl:value-of select="NumeroLicenzaGuida" />
																		</span>
																	</li>
																</xsl:if>
															</xsl:for-each>
														</ul>
													</xsl:if>

													<xsl:if
														test="DatiGenerali/DatiTrasporto/MezzoTrasporto or DatiGenerali/DatiTrasporto/CausaleTrasporto or DatiGenerali/DatiTrasporto/NumeroColli or DatiGenerali/DatiTrasporto/Descrizione or DatiGenerali/DatiTrasporto/UnitaMisuraPeso or DatiGenerali/DatiTrasporto/PesoLordo or DatiGenerali/DatiTrasporto/PesoNetto or DatiGenerali/DatiTrasporto/DataOraRitiro or DatiGenerali/DatiTrasporto/DataInizioTrasporto or DatiGenerali/DatiTrasporto/TipoResa or DatiGenerali/DatiTrasporto/IndirizzoResa">
														<h4>Altri dati</h4>

														<ul>
															<xsl:for-each select="DatiGenerali/DatiTrasporto">
																<xsl:if test="MezzoTrasporto">
																	<li>
																		Mezzo di trasporto:
																		<span>
																			<xsl:value-of select="MezzoTrasporto" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="CausaleTrasporto">
																	<li>
																		Causale trasporto:
																		<span>
																			<xsl:value-of select="CausaleTrasporto" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="NumeroColli">
																	<li>
																		Numero colli trasportati:
																		<span>
																			<xsl:value-of select="NumeroColli" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="Descrizione">
																	<li>
																		Descrizione beni trasportati:
																		<span>
																			<xsl:value-of select="Descrizione" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="UnitaMisuraPeso">
																	<li>
																		Unità di misura del peso merce:
																		<span>
																			<xsl:value-of select="UnitaMisuraPeso" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="PesoLordo">
																	<li>
																		Peso lordo:
																		<span>
																			<xsl:value-of select="PesoLordo" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="PesoNetto">
																	<li>
																		Peso netto:
																		<span>
																			<xsl:value-of select="PesoNetto" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="DataOraRitiro">
																	<li>
																		Data e ora ritiro merce:
																		<span>
																			<xsl:value-of select="DataOraRitiro" />
																		</span>
																		<xsl:call-template name="FormatDate">
																			<xsl:with-param name="DateTime" select="DataOraRitiro" />
																		</xsl:call-template>
																	</li>
																</xsl:if>
																<xsl:if test="DataInizioTrasporto">
																	<li>
																		Data inizio trasporto:
																		<span>
																			<xsl:value-of select="DataInizioTrasporto" />
																		</span>
																		<xsl:call-template name="FormatDate">
																			<xsl:with-param name="DateTime" select="DataInizioTrasporto" />
																		</xsl:call-template>
																	</li>
																</xsl:if>
																<xsl:if test="TipoResa">
																	<li>
																		Tipologia di resa:
																		<span>
																			<xsl:value-of select="TipoResa" />
																		</span>

																		(codifica secondo standard ICC)
																	</li>
																</xsl:if>
																<xsl:if test="IndirizzoResa/Indirizzo">
																	<li>
																		Indirizzo di resa:
																		<span>
																			<xsl:value-of select="IndirizzoResa/Indirizzo" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="IndirizzoResa/NumeroCivico">
																	<li>
																		Numero civico indirizzo di resa:
																		<span>
																			<xsl:value-of select="IndirizzoResa/NumeroCivico" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="IndirizzoResa/CAP">
																	<li>
																		CAP indirizzo di resa:
																		<span>
																			<xsl:value-of select="IndirizzoResa/CAP" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="IndirizzoResa/Comune">
																	<li>
																		Comune di resa:
																		<span>
																			<xsl:value-of select="IndirizzoResa/Comune" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="IndirizzoResa/Provincia">
																	<li>
																		Provincia di resa:
																		<span>
																			<xsl:value-of select="IndirizzoResa/Provincia" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="IndirizzoResa/Nazione">
																	<li>
																		Nazione di resa:
																		<span>
																			<xsl:value-of select="IndirizzoResa/Nazione" />
																		</span>
																	</li>
																</xsl:if>
															</xsl:for-each>
														</ul>
													</xsl:if>

												</div>
											</xsl:if>
											<!--FINE DATI TRASPORTO-->

											<!--INIZIO FATTURA PRINCIPALE-->
											<xsl:if test="DatiGenerali/FatturaPrincipale">
												<div id="fattura-principale">
													<h3>Dati relativi alla fattura principale</h3>
													<ul>
														<xsl:if test="DatiGenerali/FatturaPrincipale/NumeroFatturaPrincipale">
															<li>
																Numero fattura principale:
																<span>
																	<xsl:value-of select="DatiGenerali/FatturaPrincipale/NumeroFatturaPrincipale" />
																</span>
															</li>
														</xsl:if>
														<xsl:if test="DatiGenerali/FatturaPrincipale/DataFatturaPrincipale">
															<li>
																Data fattura principale:
																<span>
																	<xsl:value-of select="DatiGenerali/FatturaPrincipale/DataFatturaPrincipale" />
																</span>
																<xsl:call-template name="FormatDate">
																	<xsl:with-param name="DateTime" select="DatiGenerali/FatturaPrincipale/DataFatturaPrincipale" />
																</xsl:call-template>
															</li>
														</xsl:if>
													</ul>
												</div>
											</xsl:if>
											<!--FINE FATTURA PRINCIPALE-->

										</div>
									</xsl:if>
									<!--FINE DATI GENERALI-->

									<!--INIZIO DATI BENI E SERVIZI-->
									<xsl:if test="DatiBeniServizi">
										<div id="dati-dettaglio-linee">

											<!--INIZIO DATI DI DETTAGLIO DELLE LINEE-->
											<xsl:if test="DatiBeniServizi/DettaglioLinee">
												<div id="righe">
													<h3>Dati relativi alle linee di dettaglio della fornitura</h3>

													<xsl:for-each select="DatiBeniServizi/DettaglioLinee">
														<h5>
															Nr. linea:
															<span>
																<xsl:value-of select="NumeroLinea" />
															</span>
														</h5>

														<ul>
															<xsl:if test="TipoCessionePrestazione">
																<li>
																	Tipo cessione/prestazione:
																	<span>
																		<xsl:value-of select="TipoCessionePrestazione" />
																	</span>
																	<xsl:variable name="TCP">
																		<xsl:value-of select="TipoCessionePrestazione" />
																	</xsl:variable>
																	<xsl:choose>
																		<xsl:when test="$TCP='SC'">
																			(sconto)
																		</xsl:when>
																		<xsl:when test="$TCP='PR'">
																			(premio)
																		</xsl:when>
																		<xsl:when test="$TCP='AB'">
																			(abbuono)
																		</xsl:when>
																		<xsl:when test="$TCP='AC'">
																			(spesa accessoria)
																		</xsl:when>
																		<xsl:otherwise>
																			<span>(!!! codice non previsto !!!)</span>
																		</xsl:otherwise>
																	</xsl:choose>
																</li>
															</xsl:if>
															<xsl:if test="CodiceArticolo">
																<li>
																	<h5>Codifica articolo</h5>
																	<xsl:for-each select="CodiceArticolo">
																		<ul>
																			<xsl:if test="CodiceTipo">
																				<li>
																					Tipo:
																					<span>
																						<xsl:value-of select="CodiceTipo" />
																					</span>
																				</li>
																			</xsl:if>
																			<xsl:if test="CodiceValore">
																				<li>
																					Valore:
																					<span>
																						<xsl:value-of select="CodiceValore" />
																					</span>
																				</li>
																			</xsl:if>
																		</ul>
																	</xsl:for-each>
																</li>
															</xsl:if>
															<xsl:if test="Descrizione">
																<li>
																	Descrizione bene/servizio:
																	<span>
																		<xsl:value-of select="Descrizione" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Quantita">
																<li>
																	Quantità:
																	<span>
																		<xsl:value-of select="Quantita" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="UnitaMisura">
																<li>
																	Unità di misura:
																	<span>
																		<xsl:value-of select="UnitaMisura" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="DataInizioPeriodo">
																<li>
																	Data inizio periodo di riferimento:
																	<span>
																		<xsl:value-of select="DataInizioPeriodo" />
																	</span>
																	<xsl:call-template name="FormatDate">
																		<xsl:with-param name="DateTime" select="DataInizioPeriodo" />
																	</xsl:call-template>
																</li>
															</xsl:if>
															<xsl:if test="DataFinePeriodo">
																<li>
																	Data fine periodo di riferimento:
																	<span>
																		<xsl:value-of select="DataFinePeriodo" />
																	</span>
																	<xsl:call-template name="FormatDate">
																		<xsl:with-param name="DateTime" select="DataFinePeriodo" />
																	</xsl:call-template>
																</li>
															</xsl:if>
															<xsl:if test="PrezzoUnitario">
																<li>
																	Valore unitario:
																	<span>
																		<xsl:value-of select="PrezzoUnitario" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="ScontoMaggiorazione">
																<li>
																	<h5>Sconto/Maggiorazione</h5>

																	<xsl:for-each select="ScontoMaggiorazione">
																		<ul>
																			<xsl:if test="Tipo">
																				<li>
																					Tipo:
																					<span>
																						<xsl:value-of select="Tipo" />
																					</span>
																					<xsl:variable name="TSCM">
																						<xsl:value-of select="Tipo" />
																					</xsl:variable>
																					<xsl:choose>
																						<xsl:when test="$TSCM='SC'">

																							(sconto)
																						</xsl:when>
																						<xsl:when test="$TSCM='MG'">

																							(maggiorazione)
																						</xsl:when>
																						<xsl:otherwise>

																							<span>(!!! codice non previsto !!!)</span>
																						</xsl:otherwise>
																					</xsl:choose>
																				</li>
																			</xsl:if>
																			<xsl:if test="Percentuale">
																				<li>
																					Percentuale (%):
																					<span>
																						<xsl:value-of select="Percentuale" />
																					</span>
																				</li>
																			</xsl:if>
																			<xsl:if test="Importo">
																				<li>
																					Importo:
																					<span>
																						<xsl:value-of select="Importo" />
																					</span>
																				</li>
																			</xsl:if>
																		</ul>
																	</xsl:for-each>
																</li>
															</xsl:if>
															<xsl:if test="PrezzoTotale">
																<li>
																	Valore totale:
																	<span>
																		<xsl:value-of select="PrezzoTotale" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="AliquotaIVA">
																<li>
																	IVA (%):
																	<span>
																		<xsl:value-of select="AliquotaIVA" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Ritenuta">
																<li>
																	Soggetta a ritenuta:
																	<span>
																		<xsl:value-of select="Ritenuta" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Natura">
																<li>
																	Natura operazione:
																	<span>
																		<xsl:value-of select="Natura" />
																	</span>
																	<xsl:variable name="NAT">
																		<xsl:value-of select="Natura" />
																	</xsl:variable>
																	<xsl:choose>
																		<xsl:when test="$NAT='N1'">
																			(esclusa ex art.15)
																		</xsl:when>
																		<xsl:when test="$NAT='N2'">
																			(non soggetta)
																		</xsl:when>
																		<xsl:when test="$NAT='N2.1'">
																			(non soggette ad IVA - artt. da 7 a 7-septies 
																			del DPR 633/72)
																		</xsl:when>
																		<xsl:when test="$NAT='N2.2'">
																			(non soggette - altri casi)
																		</xsl:when>
																		<xsl:when test="$NAT='N3'">
																			(non imponibili)
																		</xsl:when>
																		<xsl:when test="$NAT='N3.1'">
																			(non imponibili - esportazioni)
																		</xsl:when>
																		<xsl:when test="$NAT='N3.2'">
																			(non imponibili - cessioni intracomunitarie)
																		</xsl:when>
																		<xsl:when test="$NAT='N3.3'">
																			(non imponibili - cessioni verso S.Marino)
																		</xsl:when>
																		<xsl:when test="$NAT='N3.4'">
																			(non imponibili - operazioni assimilate alle 
																			cessioni all'esportazione)
																		</xsl:when>
																		<xsl:when test="$NAT='N3.5'">
																			(non imponibili - a seguito di dichiarazioni 
																			d'intento)
																		</xsl:when>
																		<xsl:when test="$NAT='N3.6'">
																			(non imponibili - altre operazioni che non 
																			concorrono alla formazione del plafond)
																		</xsl:when>
																		<xsl:when test="$NAT='N4'">
																			(esenti)
																		</xsl:when>
																		<xsl:when test="$NAT='N5'">
																			(regime del margine / IVA non esposta in fattura)
																		</xsl:when>
																		<xsl:when test="$NAT='N6'">
																			(inversione contabile per le operazioni in reverse 
																			charge ovvero nei casi di autofatturazione per 
																			acquisti extra UE di servizi ovvero per importazioni 
																			di beni nei soli casi previsti)
																		</xsl:when>
																		<xsl:when test="$NAT='N6.1'">
																			(inversione contabile - cessione di rottami e 
																			altri materiali di recupero)
																		</xsl:when>
																		<xsl:when test="$NAT='N6.2'">
																			(inversione contabile - cessione di oro e 
																			argento puro)
																		</xsl:when>
																		<xsl:when test="$NAT='N6.3'">
																			(inversione contabile - subappalto nel settore 
																			edile)
																		</xsl:when>
																		<xsl:when test="$NAT='N6.4'">
																			(inversione contabile - cessione di fabbricati)
																		</xsl:when>
																		<xsl:when test="$NAT='N6.5'">
																			(inversione contabile - cessione di telefoni 
																			cellulari)
																		</xsl:when>
																		<xsl:when test="$NAT='N6.6'">
																			(inversione contabile - cessione di prodotti 
																			elettronici)
																		</xsl:when>
																		<xsl:when test="$NAT='N6.7'">
																			(inversione contabile - prestazioni comparto 
																			edile e settori connessi)
																		</xsl:when>
																		<xsl:when test="$NAT='N6.8'">
																			(inversione contabile - operazioni settore 
																			energetico)
																		</xsl:when>
																		<xsl:when test="$NAT='N6.9'">
																			(inversione contabile - altri casi)
																		</xsl:when>
																		<xsl:when test="$NAT='N7'">
																			(IVA assolta in altro stato UE - vendite a distanza 
																			ex art.40 c.3 e 4 e art.41 c.1 lett. b DL 331/93; 
																			prestazione di servizi di telecomunicazioni, 
																			tele-radiodiffusione ed elettronici ex art.7-sexies 
																			lett. f, g, e art.74-sexies DPR 633/72)
																		</xsl:when>
																		<xsl:otherwise>
																			<span>(!!! codice non previsto !!!)</span>
																		</xsl:otherwise>
																	</xsl:choose>
																</li>
															</xsl:if>
															<xsl:if test="RiferimentoAmministrazione">
																<li>
																	Riferimento amministrativo/contabile:
																	<span>
																		<xsl:value-of select="RiferimentoAmministrazione" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="AltriDatiGestionali">
																<li>
																	<h5>Altri dati gestionali</h5>
																	<ul>
																		<xsl:for-each select="AltriDatiGestionali">
																			<xsl:if test="TipoDato">
																				<li>
																					Tipo dato:
																					<span>
																						<xsl:value-of select="TipoDato" />
																					</span>
																				</li>
																			</xsl:if>
																			<xsl:if test="RiferimentoTesto">
																				<li>
																					Valore testo:
																					<span>
																						<xsl:value-of select="RiferimentoTesto" />
																					</span>
																				</li>
																			</xsl:if>
																			<xsl:if test="RiferimentoNumero">
																				<li>
																					Valore numerico:
																					<span>
																						<xsl:value-of select="RiferimentoNumero" />
																					</span>
																				</li>
																			</xsl:if>
																			<xsl:if test="RiferimentoData">
																				<li>
																					Valore data:
																					<span>
																						<xsl:value-of select="RiferimentoData" />
																					</span>
																					<xsl:call-template name="FormatDate">
																						<xsl:with-param name="DateTime" select="RiferimentoData" />
																					</xsl:call-template>
																				</li>
																			</xsl:if>
																		</xsl:for-each>
																	</ul>
																</li>
															</xsl:if>
														</ul>
													</xsl:for-each>
												</div>
											</xsl:if>
											<!--FINE DATI DI DETTAGLIO DELLE LINEE-->

											<!--INIZIO DATI DI RIEPILOGO ALIQUOTE E NATURE-->
											<xsl:if test="DatiBeniServizi/DatiRiepilogo">
												<div id="riepilogo-aliquote-nature">
													<h3>Dati di riepilogo per aliquota IVA e natura</h3>
													<xsl:for-each select="DatiBeniServizi/DatiRiepilogo">
														<ul>
															<xsl:if test="AliquotaIVA">
																<li>
																	Aliquota IVA (%):
																	<span>
																		<xsl:value-of select="AliquotaIVA" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Natura">
																<li>
																	Natura operazioni:
																	<span>
																		<xsl:value-of select="Natura" />
																	</span>
																	<xsl:variable name="NAT1">
																		<xsl:value-of select="Natura" />
																	</xsl:variable>
																	<xsl:choose>
																		<xsl:when test="$NAT1='N1'">
																			(escluse ex art.15)
																		</xsl:when>
																		<xsl:when test="$NAT1='N2'">
																			(non soggette)
																		</xsl:when>
																		<xsl:when test="$NAT1='N2.1'">
																			(non soggette ad IVA - artt. da 7 a 7-septies 
																			del DPR 633/72)
																		</xsl:when>
																		<xsl:when test="$NAT1='N2.2'">
																			(non soggette - altri casi)
																		</xsl:when>
																		<xsl:when test="$NAT1='N3'">
																			(non imponibili)
																		</xsl:when>
																		<xsl:when test="$NAT1='N3.1'">
																			(non imponibili - esportazioni)
																		</xsl:when>
																		<xsl:when test="$NAT1='N3.2'">
																			(non imponibili - cessioni intracomunitarie)
																		</xsl:when>
																		<xsl:when test="$NAT1='N3.3'">
																			(non imponibili - cessioni verso S.Marino)
																		</xsl:when>
																		<xsl:when test="$NAT1='N3.4'">
																			(non imponibili - operazioni assimilate alle 
																			cessioni all'esportazione)
																		</xsl:when>
																		<xsl:when test="$NAT1='N3.5'">
																			(non imponibili - a seguito di dichiarazioni 
																			d'intento)
																		</xsl:when>
																		<xsl:when test="$NAT1='N3.6'">
																			(non imponibili - altre operazioni che non 
																			concorrono alla formazione del plafond)
																		</xsl:when>
																		<xsl:when test="$NAT1='N4'">
																			(esenti)
																		</xsl:when>
																		<xsl:when test="$NAT1='N5'">
																			(regime del margine / IVA non esposta in fattura)
																		</xsl:when>
																		<xsl:when test="$NAT1='N6'">
																			(inversione contabile per le operazioni in reverse 
																			charge ovvero nei casi di autofatturazione per 
																			acquisti extra UE di servizi ovvero per importazioni 
																			di beni nei soli casi previsti)
																		</xsl:when>
																		<xsl:when test="$NAT1='N6.1'">
																			(inversione contabile - cessione di rottami e 
																			altri materiali di recupero)
																		</xsl:when>
																		<xsl:when test="$NAT1='N6.2'">
																			(inversione contabile - cessione di oro e 
																			argento puro)
																		</xsl:when>
																		<xsl:when test="$NAT1='N6.3'">
																			(inversione contabile - subappalto nel settore 
																			edile)
																		</xsl:when>
																		<xsl:when test="$NAT1='N6.4'">
																			(inversione contabile - cessione di fabbricati)
																		</xsl:when>
																		<xsl:when test="$NAT1='N6.5'">
																			(inversione contabile - cessione di telefoni 
																			cellulari)
																		</xsl:when>
																		<xsl:when test="$NAT1='N6.6'">
																			(inversione contabile - cessione di prodotti 
																			elettronici)
																		</xsl:when>
																		<xsl:when test="$NAT1='N6.7'">
																			(inversione contabile - prestazioni comparto 
																			edile e settori connessi)
																		</xsl:when>
																		<xsl:when test="$NAT1='N6.8'">
																			(inversione contabile - operazioni settore 
																			energetico)
																		</xsl:when>
																		<xsl:when test="$NAT1='N6.9'">
																			(inversione contabile - altri casi)
																		</xsl:when>
																		<xsl:when test="$NAT1='N7'">
																			(IVA assolta in altro stato UE - vendite a distanza 
																			ex art.40 c.3 e 4 e art.41 c.1 lett. b DL 331/93; 
																			prestazione di servizi di telecomunicazioni, 
																			tele-radiodiffusione ed elettronici ex art.7-sexies 
																			lett. f, g, e art.74-sexies DPR 633/72)
																		</xsl:when>
																		<xsl:otherwise>
																			<span>(!!! codice non previsto !!!)</span>
																		</xsl:otherwise>
																	</xsl:choose>
																</li>
															</xsl:if>
															<xsl:if test="SpeseAccessorie">
																<li>
																	Spese accessorie:
																	<span>
																		<xsl:value-of select="SpeseAccessorie" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Arrotondamento">
																<li>
																	Arrotondamento:
																	<span>
																		<xsl:value-of select="Arrotondamento" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="ImponibileImporto">
																<li>
																	Totale imponibile/importo:
																	<span>
																		<xsl:value-of select="ImponibileImporto" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="Imposta">
																<li>
																	Totale imposta:
																	<span>
																		<xsl:value-of select="Imposta" />
																	</span>
																</li>
															</xsl:if>
															<xsl:if test="EsigibilitaIVA">
																<li>
																	Esigibilità IVA:
																	<span>
																		<xsl:value-of select="EsigibilitaIVA" />
																	</span>
																	<xsl:variable name="EI">
																		<xsl:value-of select="EsigibilitaIVA" />
																	</xsl:variable>
																	<xsl:choose>
																		<xsl:when test="$EI='I'">
																			(esigibilità immediata)
																		</xsl:when>
																		<xsl:when test="$EI='D'">
																			(esigibilità differita)
																		</xsl:when>
																		<xsl:when test="$EI='S'">
																			(scissione dei pagamenti)
																		</xsl:when>
																		<xsl:otherwise>
																			<span>(!!! codice non previsto !!!)</span>
																		</xsl:otherwise>
																	</xsl:choose>
																</li>
															</xsl:if>
															<xsl:if test="RiferimentoNormativo">
																<li>
																	Riferimento normativo:
																	<span>
																		<xsl:value-of select="RiferimentoNormativo" />
																	</span>
																</li>
															</xsl:if>
														</ul>
													</xsl:for-each>
												</div>
											</xsl:if>
											<!--FINE DATI RIEPILOGO ALIQUOTE E NATURE-->

										</div>
									</xsl:if>
									<!--FINE DATI BENI E SERVIZI-->

									<!--INIZIO DATI VEICOLI-->
									<xsl:if test="DatiVeicoli">
										<div id="dati-veicoli">
											<h3>Dati Veicoli ex art. 38 dl 331/1993</h3>
											<ul>
												<xsl:for-each select="DatiVeicoli">
													<xsl:if test="Data">
														<li>
															Data prima immatricolazione / iscrizione PR:
															<span>
																<xsl:value-of select="Data" />
															</span>
															<xsl:call-template name="FormatDate">
																<xsl:with-param name="DateTime" select="Data" />
															</xsl:call-template>
														</li>
													</xsl:if>
													<xsl:if test="TotalePercorso">
														<li>
															Totale percorso:
															<span>
																<xsl:value-of select="TotalePercorso" />
															</span>
														</li>
													</xsl:if>
												</xsl:for-each>
											</ul>
										</div>
									</xsl:if>
									<!--FINE DATI VEICOLI-->

									<!--INIZIO DATI PAGAMENTO-->
									<xsl:if test="DatiPagamento">
										<div id="dati-pagamento-condizioni">
											<h3>Dati relativi al pagamento</h3>
											<ul>
												<xsl:for-each select="DatiPagamento">
													<xsl:if test="CondizioniPagamento">
														<li>
															Condizioni di pagamento:
															<span>
																<xsl:value-of select="CondizioniPagamento" />
															</span>
															<xsl:variable name="CP">
																<xsl:value-of select="CondizioniPagamento" />
															</xsl:variable>
															<xsl:choose>
																<xsl:when test="$CP='TP01'">
																	(pagamento a rate)
																</xsl:when>
																<xsl:when test="$CP='TP02'">
																	(pagamento completo)
																</xsl:when>
																<xsl:when test="$CP='TP03'">
																	(anticipo)
																</xsl:when>
																<xsl:when test="$CP=''">
																</xsl:when>
																<xsl:otherwise>
																	<span>(!!! codice non previsto !!!)</span>
																</xsl:otherwise>
															</xsl:choose>
														</li>
													</xsl:if>

													<xsl:if test="DettaglioPagamento">
														<h5>Dettaglio pagamento</h5>

														<xsl:for-each select="DettaglioPagamento">
															<ul>
																<xsl:if test="Beneficiario">
																	<li>
																		Beneficiario del pagamento:
																		<span>
																			<xsl:value-of select="Beneficiario" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="ModalitaPagamento">
																	<li>
																		Modalità:
																		<span>
																			<xsl:value-of select="ModalitaPagamento" />
																		</span>
																		<xsl:variable name="MP">
																			<xsl:value-of select="ModalitaPagamento" />
																		</xsl:variable>
																		<xsl:choose>
																			<xsl:when test="$MP='MP01'">
																				(contanti)
																			</xsl:when>
																			<xsl:when test="$MP='MP02'">
																				(assegno)
																			</xsl:when>
																			<xsl:when test="$MP='MP03'">
																				(assegno circolare)
																			</xsl:when>
																			<xsl:when test="$MP='MP04'">
																				(contanti presso Tesoreria)
																			</xsl:when>
																			<xsl:when test="$MP='MP05'">
																				(bonifico)
																			</xsl:when>
																			<xsl:when test="$MP='MP06'">
																				(vaglia cambiario)
																			</xsl:when>
																			<xsl:when test="$MP='MP07'">
																				(bollettino bancario)
																			</xsl:when>
																			<xsl:when test="$MP='MP08'">
																				(carta di pagamento)
																			</xsl:when>
																			<xsl:when test="$MP='MP09'">
																				(RID)
																			</xsl:when>
																			<xsl:when test="$MP='MP10'">
																				(RID utenze)
																			</xsl:when>
																			<xsl:when test="$MP='MP11'">
																				(RID veloce)
																			</xsl:when>
																			<xsl:when test="$MP='MP12'">
																				(RIBA)
																			</xsl:when>
																			<xsl:when test="$MP='MP13'">
																				(MAV)
																			</xsl:when>
																			<xsl:when test="$MP='MP14'">
																				(quietanza erario)
																			</xsl:when>
																			<xsl:when test="$MP='MP15'">
																				(giroconto su conti di contabilità speciale)
																			</xsl:when>
																			<xsl:when test="$MP='MP16'">
																				(domiciliazione bancaria)
																			</xsl:when>
																			<xsl:when test="$MP='MP17'">
																				(domiciliazione postale)
																			</xsl:when>
																			<xsl:when test="$MP='MP18'">
																				(bollettino di c/c postale)
																			</xsl:when>
																			<xsl:when test="$MP='MP19'">
																				(SEPA Direct Debit)
																			</xsl:when>
																			<xsl:when test="$MP='MP20'">
																				(SEPA Direct Debit CORE)
																			</xsl:when>
																			<xsl:when test="$MP='MP21'">
																				(SEPA Direct Debit B2B)
																			</xsl:when>
																			<xsl:when test="$MP='MP22'">
																				(Trattenuta su somme già riscosse)
																			</xsl:when>
																			<xsl:when test="$MP='MP23'">
																				(PagoPA)
																			</xsl:when>
																			<xsl:when test="$MP=''">
																			</xsl:when>
																			<xsl:otherwise>
																				<span>(!!! codice non previsto !!!)</span>
																			</xsl:otherwise>
																		</xsl:choose>
																	</li>
																</xsl:if>
																<xsl:if test="DataRiferimentoTerminiPagamento">
																	<li>
																		Decorrenza termini di pagamento:
																		<span>
																			<xsl:value-of select="DataRiferimentoTerminiPagamento" />
																		</span>
																		<xsl:call-template name="FormatDate">
																			<xsl:with-param name="DateTime" select="DataRiferimentoTerminiPagamento" />
																		</xsl:call-template>
																	</li>
																</xsl:if>
																<xsl:if test="GiorniTerminiPagamento">
																	<li>
																		Termini di pagamento (in giorni):
																		<span>
																			<xsl:value-of select="GiorniTerminiPagamento" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="DataScadenzaPagamento">
																	<li>
																		Data scadenza pagamento:
																		<span>
																			<xsl:value-of select="DataScadenzaPagamento" />
																		</span>
																		<xsl:call-template name="FormatDate">
																			<xsl:with-param name="DateTime" select="DataScadenzaPagamento" />
																		</xsl:call-template>
																	</li>
																</xsl:if>
																<xsl:if test="ImportoPagamento">
																	<li>
																		Importo:
																		<span>
																			<xsl:value-of select="ImportoPagamento" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="CodUfficioPostale">
																	<li>
																		Codice Ufficio Postale:
																		<span>
																			<xsl:value-of select="CodUfficioPostale" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="CognomeQuietanzante">
																	<li>
																		Cognome del quietanzante:
																		<span>
																			<xsl:value-of select="CognomeQuietanzante" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="NomeQuietanzante">
																	<li>
																		Nome del quietanzante:
																		<span>
																			<xsl:value-of select="NomeQuietanzante" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="CFQuietanzante">
																	<li>
																		CF del quietanzante:
																		<span>
																			<xsl:value-of select="CFQuietanzante" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="TitoloQuietanzante">
																	<li>
																		Titolo del quietanzante:
																		<span>
																			<xsl:value-of select="TitoloQuietanzante" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="IstitutoFinanziario">
																	<li>
																		Istituto finanziario:
																		<span>
																			<xsl:value-of select="IstitutoFinanziario" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="IBAN">
																	<li>
																		Codice IBAN:
																		<span>
																			<xsl:value-of select="IBAN" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="ABI">
																	<li>
																		Codice ABI:
																		<span>
																			<xsl:value-of select="ABI" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="CAB">
																	<li>
																		Codice CAB:
																		<span>
																			<xsl:value-of select="CAB" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="BIC">
																	<li>
																		Codice BIC:
																		<span>
																			<xsl:value-of select="BIC" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="ScontoPagamentoAnticipato">
																	<li>
																		Sconto per pagamento anticipato:
																		<span>
																			<xsl:value-of select="ScontoPagamentoAnticipato" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="DataLimitePagamentoAnticipato">
																	<li>
																		Data limite per il pagamento anticipato:
																		<span>
																			<xsl:value-of select="DataLimitePagamentoAnticipato" />
																		</span>
																		<xsl:call-template name="FormatDate">
																			<xsl:with-param name="DateTime" select="DataLimitePagamentoAnticipato" />
																		</xsl:call-template>
																	</li>
																</xsl:if>
																<xsl:if test="PenalitaPagamentiRitardati">
																	<li>
																		Penale per ritardato pagamento:
																		<span>
																			<xsl:value-of select="PenalitaPagamentiRitardati" />
																		</span>
																	</li>
																</xsl:if>
																<xsl:if test="DataDecorrenzaPenale">
																	<li>
																		Data di decorrenza della penale:
																		<span>
																			<xsl:value-of select="DataDecorrenzaPenale" />
																		</span>
																		<xsl:call-template name="FormatDate">
																			<xsl:with-param name="DateTime" select="DataDecorrenzaPenale" />
																		</xsl:call-template>
																	</li>
																</xsl:if>
																<xsl:if test="CodicePagamento">
																	<li>
																		Codice pagamento:
																		<span>
																			<xsl:value-of select="CodicePagamento" />
																		</span>
																	</li>
																</xsl:if>
															</ul>
														</xsl:for-each>
													</xsl:if>
												</xsl:for-each>
											</ul>

										</div>
									</xsl:if>
									<!--FINE DATI PAGAMENTO-->

									<!--INIZIO ALLEGATI-->
									<xsl:if test="Allegati">
										<div id="allegati">
											<h3>Dati relativi agli allegati</h3>

											<xsl:for-each select="Allegati">
												<ul>
													<xsl:if test="NomeAttachment">
														<li>
															Nome dell'allegato:
															<span>
																<xsl:value-of select="NomeAttachment" />
															</span>
														</li>
													</xsl:if>
													<xsl:if test="AlgoritmoCompressione">
														<li>
															Algoritmo di compressione:
															<span>
																<xsl:value-of select="AlgoritmoCompressione" />
															</span>
														</li>
													</xsl:if>
													<xsl:if test="FormatoAttachment">
														<li>
															Formato:
															<span>
																<xsl:value-of select="FormatoAttachment" />
															</span>
														</li>
													</xsl:if>
													<xsl:if test="DescrizioneAttachment">
														<li>
															Descrizione:
															<span>
																<xsl:value-of select="DescrizioneAttachment" />
															</span>
														</li>
													</xsl:if>
												</ul>
											</xsl:for-each>
										</div>
									</xsl:if>
									<!--FINE ALLEGATI-->

									<div class="footer">
										Versione prodotta con foglio di stile SdI
										<a href="http://www.fatturapa.gov.it">www.fatturapa.gov.it</a>
									</div>
								</div>
							</xsl:for-each>
							<!--FINE BODY-->

						</div>
					</xsl:if>
				</div>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>