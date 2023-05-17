<?xml version="1.0"?>
<xsl:stylesheet 
	version="1.1" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:a="http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.0">
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
					<xsl:if test="a:FatturaElettronicaSemplificata">

						<div id="fattura-elettronica">

							<h1>FATTURA ELETTRONICA</h1>

							<xsl:if test="a:FatturaElettronicaSemplificata/FatturaElettronicaHeader">
								<div class="page">
									<div class="versione">
										Versione <xsl:value-of select="a:FatturaElettronicaSemplificata/@versione"/>
									</div>

									<xsl:if test="a:FatturaElettronicaSemplificata/FatturaElettronicaHeader/DatiTrasmissione">
										<!--INIZIO DATI DELLA TRASMISSIONE-->
										<div id="dati-trasmissione">
											<h3>Dati relativi alla trasmissione</h3>
											<ul>
												<xsl:for-each select="a:FatturaElettronicaSemplificata/FatturaElettronicaHeader/DatiTrasmissione">

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
															Codice Amministrazione destinataria:
															<span>
																<xsl:value-of select="CodiceDestinatario" />
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
									<xsl:if test="a:FatturaElettronicaSemplificata/FatturaElettronicaHeader/CedentePrestatore">
										<div id="cedente">
											<h3>Dati del cedente / prestatore</h3>
											<ul>
												<xsl:for-each select="a:FatturaElettronicaSemplificata/FatturaElettronicaHeader/CedentePrestatore">
														
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
											
											<xsl:if test="Sede">
												<h4>Dati della sede</h4>
												<ul>
													<xsl:for-each select="Sede">
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
											
											
											<xsl:if test="StabileOrganizzazione">
												<h4>Dati della stabile organizzazione</h4>
												<ul>
													<xsl:for-each select="StabileOrganizzazione">
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
											
											
											
											<xsl:if test="RappresentanteFiscale">
												<h4>Dati del rappresentante fiscale del cedente / prestatore</h4>

												<ul>
													<xsl:for-each select="RappresentanteFiscale">
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
											</xsl:if>
											
											<xsl:if test="IscrizioneREA">
												<h4>Dati di iscrizione nel registro delle imprese</h4>

												<ul>
													<xsl:for-each select="IscrizioneREA">
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
											
											
											
											<xsl:if test="RegimeFiscale">
												<h4>Regime fiscale</h4>
												<ul>
												
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
												</ul>
											</xsl:if>

												</xsl:for-each>
											
											</ul>
										</div>
									</xsl:if>
									<!--FINE DATI CEDENTE PRESTATORE-->

									

									<!--INIZIO DATI CESSIONARIO COMMITTENTE-->
									<xsl:if test="a:FatturaElettronicaSemplificata/FatturaElettronicaHeader/CessionarioCommittente">
										<div id="cessionario">
											<h3>Dati del cessionario / committente</h3>
											<ul>
											
										<xsl:for-each select="a:FatturaElettronicaSemplificata/FatturaElettronicaHeader/CessionarioCommittente">
												
											<xsl:if test="IdentificativiFiscali">
												<h4>Dati fiscali</h4>

												<ul>
													<xsl:for-each select="IdentificativiFiscali">
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
													</xsl:for-each>
												</ul>
											</xsl:if>


											<xsl:if test="AltriDatiIdentificativi">
												<h4>Altri dati identificativi</h4>	

												<ul>
												<xsl:for-each select="AltriDatiIdentificativi">
													
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
														<xsl:if test="Sede">
												<h4>Dati della sede</h4>
												<ul>
													<xsl:for-each select="Sede">
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
											
											
											<xsl:if test="StabileOrganizzazione">
												<h4>Dati della stabile organizzazione</h4>
												<ul>
													<xsl:for-each select="StabileOrganizzazione">
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
											
											
											
											<xsl:if test="RappresentanteFiscale">
												<h4>Dati del rappresentante fiscale del cedente / prestatore</h4>

												<ul>
													<xsl:for-each select="RappresentanteFiscale">
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
											</xsl:if>											
													</xsl:for-each>
												</ul>
											</xsl:if>
												</xsl:for-each>
											</ul>
										</div>
									</xsl:if>
									<!--FINE DATI CESSIONARIO COMMITTENTE-->
									
									
									

									<!--INIZIO DATI SOGGETTO EMITTENTE-->
									<xsl:if test="a:FatturaElettronicaSemplificata/FatturaElettronicaHeader/SoggettoEmittente">
										<div id="soggetto-emittente">
											<h3>Soggetto emittente la fattura</h3>
											<ul>
												<li>
													Soggetto emittente:
													<span>
														<xsl:value-of select="a:FatturaElettronicaSemplificata/FatturaElettronicaHeader/SoggettoEmittente" />
													</span>
													<xsl:variable name="SC">
														<xsl:value-of select="a:FatturaElettronicaSemplificata/FatturaElettronicaHeader/SoggettoEmittente" />
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
							
						<xsl:if test="a:FatturaElettronicaSemplificata/FatturaElettronicaBody">
								<div class="page">
									<div class="versione">
										Versione <xsl:value-of select="a:FatturaElettronicaSemplificata/@versione"/>
									</div>

							<!--INIZIO DATI BODY-->

							<xsl:variable name="TOTALBODY">
								<xsl:value-of select="count(a:FatturaElettronicaSemplificata/FatturaElettronicaBody)" />
							</xsl:variable>

							<xsl:for-each select="a:FatturaElettronicaSemplificata/FatturaElettronicaBody">
								<xsl:if test="$TOTALBODY>1">
									<h2>
										Numero documento nel lotto:
										<xsl:value-of select="position()" />
									</h2>
								</xsl:if>
									
									
									
									

									<xsl:if test="DatiGenerali">
									
									
										<!--INIZIO DATI GENERALI-->
										<div id="dati-generali" >

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
																	<xsl:when test="$TD='TD07'">
																		(fattura semplificata)
																	</xsl:when>
																	<xsl:when test="$TD='TD08'">
																		(nota di credito semplificata)
																	</xsl:when>
																	<xsl:when test="$TD='TD09'">
																		(nota di debito semplificata)
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
														<!-- INIZIO DATI DEL BOLLO -->
														<xsl:if test="DatiGenerali/DatiGeneraliDocumento/DatiBollo">
														<div id="dati-bollo">
														<xsl:for-each select="DatiGenerali/DatiGeneraliDocumento/DatiBollo">
														<h4>Bollo</h4>
														<ul>
														<xsl:if test="BolloVirtuale">
															<li>
															Bollo virtuale:
																<span>
																	<xsl:value-of select="BolloVirtuale"/>
																</span>
															</li>
														</xsl:if>
														</ul>
														</xsl:for-each>
														</div>
														</xsl:if>
														<!-- FINE DATI DEL BOLLO -->
													</ul>	
												</div>
											</xsl:if>
											<!--FINE DATI GENERALI DOCUMENTO-->
											

													<!--INIZIO DATI DELLA FATTURA RETTIFICATA-->
													<xsl:if test="DatiGenerali/DatiFatturaRettificata">
														<div id="dati-fattura-rettificata">
															<xsl:for-each select="DatiGenerali/DatiFatturaRettificata">
																<h3>Dati fattura rettificata</h3>
																<ul>
																	<xsl:if test="NumeroFR">
																		<li>
																			Numero fattura rettificata:
																			<span>
																				<xsl:value-of select="NumeroFR" />
																			</span>
																		</li>
																	</xsl:if>	
																	<xsl:if test="DataFR">
																		<li>
																			Data fattura rettificata:
																			<span>
																				<xsl:value-of select="DataFR" />
																			</span>
																			<xsl:call-template name="FormatDate">
																				<xsl:with-param name="DateTime" select="DataFR" />
																			</xsl:call-template>
																		</li>
																	</xsl:if>	
																	<xsl:if test="ElementiRettificati">
																		<li>
																			Elementi rettificati:
																			<span>
																				<xsl:value-of select="ElementiRettificati" />
																			</span>
																		</li>
																	</xsl:if>	
																</ul>
															</xsl:for-each>
														</div>
													</xsl:if>
													<!--FINE DATI DELLA FATTURA RETTIFICATA-->		

										</div>									
									<!--FINE DATI GENERALI-->

                                    

												<!--INIZIO DATI BENI E SERVIZI-->
												    <xsl:if test="DatiBeniServizi">
													  <div id="Dati-beni-servizio">
														<h3>Dati beni servizi</h3>		
														
														<ul>
														<xsl:for-each select="DatiBeniServizi">
																	
													

			                                            <xsl:if test="Descrizione">
			                                            <li>
															
																<xsl:if test="Descrizione">
																		
																			Descrizione bene/servizio:
																			<span>
																				<xsl:value-of select="Descrizione" />
																			</span>
																</xsl:if>
																		</li>
														</xsl:if>
														
														<xsl:if test="Importo">
															
																<xsl:if test="Importo">
																		<li>
																			Importo bene/servizio:
																			<span>
																				<xsl:value-of select="Importo" />
																			</span>
																		</li>
																</xsl:if>
														</xsl:if>	
														<xsl:if test="DatiIVA/Imposta">
															
																<xsl:if test="DatiIVA/Imposta">
																		<li>
																			Ammontare imposta bene/servizio:
																			<span>
																				<xsl:value-of select="DatiIVA/Imposta" />
																			</span>
																		</li>
																</xsl:if>
														</xsl:if>
														<xsl:if test="DatiIVA/Aliquota">
															
																<xsl:if test="DatiIVA/Aliquota">
																		<li>
																			Aliquota IVA (%):
																			<span>
																				<xsl:value-of select="DatiIVA/Aliquota" />
																			</span>
																		</li>
																</xsl:if>
														</xsl:if>
														<xsl:if test="Natura">
															
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
																				<xsl:when test="$NAT1='N1'"> (escluse ex art. 15) </xsl:when>
																				<xsl:when test="$NAT1='N2'"> (non soggette) </xsl:when>
																				<xsl:when test="$NAT1='N2.1'"> (non soggette ad IVA - artt. da 7 a 7-septies del DPR 633/72) </xsl:when>
																				<xsl:when test="$NAT1='N2.2'"> (non soggette - altri casi) </xsl:when>
																				<xsl:when test="$NAT1='N3'"> (non imponibili) </xsl:when>
																				<xsl:when test="$NAT1='N3.1'"> (non imponibili - esportazioni) </xsl:when>
																				<xsl:when test="$NAT1='N3.2'"> (non imponibili - cessioni intracomunitarie) </xsl:when>
																				<xsl:when test="$NAT1='N3.3'"> (non imponibili - cessioni verso S.Marino) </xsl:when>
																				<xsl:when test="$NAT1='N3.4'"> (non imponibili - operazioni assimilate alle cessioni all'esportazione) </xsl:when>
																				<xsl:when test="$NAT1='N3.5'"> (non imponibili - a seguito di dichiarazioni d'intento) </xsl:when>
																				<xsl:when test="$NAT1='N3.6'"> (non imponibili - altre operazioni che non concorrono alla formazione del plafond) </xsl:when>
																				<xsl:when test="$NAT1='N4'"> (esenti) </xsl:when>
																				<xsl:when test="$NAT1='N5'"> (regime del margine / IVA non esposta in fattura) </xsl:when>
																				<xsl:otherwise>
																					<span>(!!! codice non previsto !!!)</span>
																				</xsl:otherwise>
																			</xsl:choose>
																		</li>
																</xsl:if>
														</xsl:if>
														<xsl:if test="RiferimentoNormativo">
															
																<xsl:if test="RiferimentoNormativo">
																		<li>
																			Riferimento normativo bene/servizio:
																			<span>
																				<xsl:value-of select="RiferimentoNormativo" />
																			</span>
																		</li>
																</xsl:if>
														</xsl:if>
															</xsl:for-each>	
																</ul>
														</div>
													</xsl:if>																		
									<!--FINE DATI BENI E SERVIZI-->
									
									
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
								

									
								    </xsl:if>							  
								</xsl:for-each>
								<div class="footer">
										Versione prodotta con foglio di stile SdI
										<a href="http://www.fatturapa.gov.it">www.fatturapa.gov.it</a>
									</div>
							
								</div>
							<!--FINE BODY-->	
							</xsl:if>							
						  </div>	
						</xsl:if>

				 </div>		
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>