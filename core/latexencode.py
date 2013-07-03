# -*- coding: utf-8 -*-

import unicodedata;

from core.blogger import logger;


#
# CHARACTER MAP TAKEN FROM latexcodec 0.2, by Peter Troeger
#    https://pypi.python.org/pypi/latexcodec
#

# generated by genmapping.py
utf82latex={
34:"''", 	# character "
35:'\\#', 	# character #
36:'\\$', 	# character $
37:'\\%', 	# character %
38:'\\&', 	# character &
95:'\\_', 	# character _
123:'\\{', 	# character {
125:'\\}', 	# character }
160:'~', 	# character  
161:'\\textexclamdown', 	# character ¡
162:'\\textcent', 	# character ¢
163:'\\textsterling', 	# character £
164:'\\textcurrency', 	# character €
165:'\\textyen', 	# character ¥
166:'\\textbrokenbar', 	# character Š
167:'\\textsection', 	# character §
168:'\\textasciidieresis', 	# character š
169:'\\textcopyright', 	# character ©
170:'\\textordfeminine', 	# character ª
171:'\\guillemotleft', 	# character «
172:'\\textlnot', 	# character ¬
174:'\\textregistered', 	# character ®
175:'\\textasciimacron', 	# character ¯
176:'\\textdegree', 	# character °
177:'\\textpm', 	# character ±
178:'\\texttwosuperior', 	# character ²
179:'\\textthreesuperior', 	# character ³
180:'\\textasciiacute', 	# character Ž
181:'\\textmu', 	# character µ
182:'\\textparagraph', 	# character ¶
183:'\\textperiodcentered', 	# character ·
185:'\\textonesuperior', 	# character ¹
186:'\\textordmasculine', 	# character º
187:'\\guillemotright', 	# character »
188:'\\textonequarter', 	# character Œ
189:'\\textonehalf', 	# character œ
190:'\\textthreequarters', 	# character Ÿ
191:'\\textquestiondown', 	# character ¿
192:'\\`A', 	# character À
193:"\\'A", 	# character Á
194:'\\^A', 	# character Â
195:'\\~A', 	# character Ã
196:'\\"A', 	# character Ä
197:'\\r{A}', 	# character Å
198:'\\AE', 	# character Æ
199:'\\c{C}', 	# character Ç
200:'\\`E', 	# character È
201:"\\'E", 	# character É
202:'\\^E', 	# character Ê
203:'\\"E', 	# character Ë
204:'\\`I', 	# character Ì
205:"\\'I", 	# character Í
206:'\\^I', 	# character Î
207:'\\"I', 	# character Ï
208:'\\DH', 	# character Ð
209:'\\~N', 	# character Ñ
210:'\\`O', 	# character Ò
211:"\\'O", 	# character Ó
212:'\\^O', 	# character Ô
213:'\\~O', 	# character Õ
214:'\\"O', 	# character Ö
215:'\\texttimes', 	# character ×
216:'\\O', 	# character Ø
217:'\\`U', 	# character Ù
218:"\\'U", 	# character Ú
219:'\\^U', 	# character Û
220:'\\"U', 	# character Ü
221:"\\'Y", 	# character Ý
222:'\\TH', 	# character Þ
223:'\\ss', 	# character ß
224:'\\`a', 	# character à
225:"\\'a", 	# character á
226:'\\^a', 	# character â
227:'\\~a', 	# character ã
228:'\\"a', 	# character ä
229:'\\r{a}', 	# character å
230:'\\ae', 	# character æ
231:'\\c{c}', 	# character ç
232:'\\`e', 	# character è
233:"\\'e", 	# character é
234:'\\^e', 	# character ê
235:'\\"e', 	# character ë
236:'\\`\\i', 	# character ì
237:"\\'\\i", 	# character í
238:'\\^\\i', 	# character î
239:'\\"\\i', 	# character ï
240:'\\dh', 	# character ð
241:'\\~n', 	# character ñ
242:'\\`o', 	# character ò
243:"\\'o", 	# character ó
244:'\\^o', 	# character ô
245:'\\~o', 	# character õ
246:'\\"o', 	# character ö
247:'\\textdiv', 	# character ÷
248:'\\o', 	# character ø
249:'\\`u', 	# character ù
250:"\\'u", 	# character ú
251:'\\^u', 	# character û
252:'\\"u', 	# character ü
253:"\\'y", 	# character ý
254:'\\th', 	# character þ
255:'\\"y', 	# character ÿ
256:'\\={A}', 	# character -DÀ-A
257:'\\={a}', 	# character -Dà-A
258:'\\u{A}', 	# character -BÃ-A
259:'\\u{a}', 	# character -Bã-A
260:'\\k{A}', 	# character -B¡-A
261:'\\k{a}', 	# character -B±-A
262:"\\'C", 	# character -BÆ-A
263:"\\'c", 	# character -Bæ-A
264:'\\^{C}', 	# character -CÆ-A
265:'\\^{c}', 	# character -Cæ-A
266:'\\.{C}', 	# character -CÅ-A
267:'\\.{c}', 	# character -Cå-A
268:'\\v{C}', 	# character -BÈ-A
269:'\\v{c}', 	# character -Bè-A
270:'\\v{D}', 	# character -BÏ-A
271:'\\v{d}', 	# character -Bï-A
272:'\\DJ', 	# character -BÐ-A
273:'\\dj', 	# character -Bð-A
274:'\\={E}', 	# character -Dª-A
275:'\\={e}', 	# character -Dº-A
276:'\\u{E}', 	# character ?
277:'\\u{e}', 	# character ?
278:'\\.{E}', 	# character -DÌ-A
279:'\\.{e}', 	# character -Dì-A
280:'\\k{E}', 	# character -BÊ-A
281:'\\k{e}', 	# character -Bê-A
282:'\\v{E}', 	# character -BÌ-A
283:'\\v{e}', 	# character -Bì-A
284:'\\^{G}', 	# character -CØ-A
285:'\\^{g}', 	# character -Cø-A
286:'\\u{G}', 	# character -C«-A
287:'\\u{g}', 	# character -C»-A
288:'\\.{G}', 	# character -CÕ-A
289:'\\.{g}', 	# character -Cõ-A
290:'\\c{G}', 	# character -D«-A
291:'\\c{g}', 	# character -D»-A
292:'\\^{H}', 	# character -CŠ-A
293:'\\^{h}', 	# character -C¶-A
294:'\\={H}', 	# character -C¡-A
295:'\\={h}', 	# character -C±-A
296:'\\~{I}', 	# character -D¥-A
297:'\\~{i}', 	# character -Dµ-A
298:'\\={I}', 	# character -DÏ-A
299:'\\={i}', 	# character -Dï-A
300:'\\u{I}', 	# character ?
301:'\\u{i}', 	# character ?
302:'\\k{I}', 	# character -DÇ-A
303:'\\k{i}', 	# character -Dç-A
304:'\\.I', 	# character -C©-A
305:'\\i', 	# character -C¹-A
306:'\\IJ', 	# character $(D)&(B
307:'\\ij', 	# character $(D)F(B
308:'\\^{J}', 	# character -C¬-A
309:'\\^{j}', 	# character -CŒ-A
310:'\\c{K}', 	# character -DÓ-A
311:'\\c{k}', 	# character -Dó-A
312:'\\textsc\{k\}', 	# character -D¢ LATIN SMALL LETTER KRA, didn't find a good latex replacement.-A
313:"\\'L", 	# character -BÅ-A
314:"\\'l", 	# character -Bå-A
315:'\\c{L}', 	# character -DŠ-A
316:'\\c{l}', 	# character -D¶-A
317:'\\v{L}', 	# character -B¥-A
318:'\\v{l}', 	# character -Bµ-A
319:'\\.{L}', 	# character $(D))(B
320:'\\.{l}', 	# character $(D)I(B
321:'\\L', 	# character -B£-A
322:'\\l', 	# character -B³-A
323:"\\'N", 	# character -BÑ-A
324:"\\'n", 	# character -Bñ-A
325:'\\c{N}', 	# character -DÑ-A
326:'\\c{n}', 	# character -Dñ-A
327:'\\v{N}', 	# character -BÒ-A
328:'\\v{n}', 	# character -Bò-A
329:'\\nument{149}', 	# character $(D)J(B
330:'\\NG', 	# character -Dœ-A
331:'\\ng', 	# character -D¿-A
332:'\\={O}', 	# character -DÒ-A
333:'\\={o}', 	# character -Dò-A
334:'\\u{O}', 	# character ?
335:'\\u{o}', 	# character ?
336:"\\'{O}", 	# character -BÕ-A
337:"\\'{o}", 	# character -Bõ-A
338:'\\OE', 	# character -bŒ-A
339:'\\oe', 	# character -bœ-A
340:"\\'R", 	# character -BÀ-A
341:"\\'r", 	# character -Bà-A
342:'\\c{R}', 	# character -D£-A
343:'\\c{r}', 	# character -D³-A
344:'\\v{R}', 	# character -BØ-A
345:'\\v{r}', 	# character -Bø-A
346:"\\'S", 	# character -BŠ-A
347:"\\'s", 	# character -B¶-A
348:'\\^{S}', 	# character -CÞ-A
349:'\\^{s}', 	# character -Cþ-A
350:'\\c{S}', 	# character -Bª-A
351:'\\c{s}', 	# character -Bº-A
352:'\\v{S}', 	# character -B©-A
353:'\\v{s}', 	# character -B¹-A
354:'\\c{T}', 	# character -BÞ-A
355:'\\c{t}', 	# character -Bþ-A
356:'\\v{T}', 	# character -B«-A
357:'\\v{t}', 	# character -B»-A
358:'\\={T}', 	# character -D¬-A
359:'\\={t}', 	# character -DŒ-A
360:'\\~{U}', 	# character -DÝ-A
361:'\\~{u}', 	# character -Dý-A
362:'\\={U}', 	# character -DÞ-A
363:'\\={u}', 	# character -Dþ-A
364:'\\u{U}', 	# character -CÝ-A
365:'\\u{u}', 	# character -Cý-A
366:'\\r{U}', 	# character -BÙ-A
367:'\\r{u}', 	# character -Bù-A
368:"\\'{U}", 	# character -BÛ-A
369:"\\'{u}", 	# character -Bû-A
370:'\\k{U}', 	# character -DÙ-A
371:'\\k{u}', 	# character -Dù-A
372:'\\^{W}', 	# character -_Ð-A
373:'\\^{w}', 	# character -_ð-A
374:'\\^{Y}', 	# character -_Þ-A
375:'\\^{y}', 	# character -_þ-A
376:'\\"Y', 	# character -_¯-A
377:"\\'Z", 	# character -B¬-A
378:"\\'z", 	# character -BŒ-A
379:'\\.Z', 	# character -B¯-A
380:'\\.z', 	# character -B¿-A
381:'\\v{Z}', 	# character -B®-A
382:'\\v{z}', 	# character -BŸ-A
402:'\\textflorin', 	# character ?
710:'\\textasciicircum', 	# character ?
711:'\\textasciicaron', 	# character -B·-A
728:'\\textasciibreve', 	# character -B¢-A
732:'\\textasciitilde', 	# character ?
733:'\\textacutedbl', 	# character -Bœ-A
1024:'\\`\\CYRE', 	# character ?
1025:'\\CYRYO', 	# character -L¡-A
1026:'\\CYRDJE', 	# character -L¢-A
1027:'\\`\\CYRG', 	# character -L£-A
1028:'\\CYRIE', 	# character -L€-A
1029:'\\CYRDZE', 	# character -L¥-A
1030:'\\CYRII', 	# character -LŠ-A
1031:'\\CYRYI', 	# character -L§-A
1032:'\\CYRJE', 	# character -Lš-A
1033:'\\CYRLJE', 	# character -L©-A
1034:'\\CYRNJE', 	# character -Lª-A
1035:'\\CYRTSHE', 	# character -L«-A
1036:'\\`\\CYRK', 	# character -L¬-A
1037:'\\`\\CYRI', 	# character ?
1038:'\\CYRUSHRT', 	# character -L®-A
1039:'\\CYRDZHE', 	# character -L¯-A
1040:'\\CYRA', 	# character -L°-A
1041:'\\CYRB', 	# character -L±-A
1042:'\\CYRV', 	# character -L²-A
1043:'\\CYRG', 	# character -L³-A
1044:'\\CYRD', 	# character -LŽ-A
1045:'\\CYRE', 	# character -Lµ-A
1046:'\\CYRZH', 	# character -L¶-A
1047:'\\CYRZ', 	# character -L·-A
1048:'\\CYRI', 	# character -Lž-A
1049:'\\CYRISHRT', 	# character -L¹-A
1050:'\\CYRK', 	# character -Lº-A
1051:'\\CYRL', 	# character -L»-A
1052:'\\CYRM', 	# character -LŒ-A
1053:'\\CYRN', 	# character -Lœ-A
1054:'\\CYRO', 	# character -LŸ-A
1055:'\\CYRP', 	# character -L¿-A
1056:'\\CYRR', 	# character -LÀ-A
1057:'\\CYRS', 	# character -LÁ-A
1058:'\\CYRT', 	# character -LÂ-A
1059:'\\CYRU', 	# character -LÃ-A
1060:'\\CYRF', 	# character -LÄ-A
1061:'\\CYRH', 	# character -LÅ-A
1062:'\\CYRC', 	# character -LÆ-A
1063:'\\CYRCH', 	# character -LÇ-A
1064:'\\CYRSH', 	# character -LÈ-A
1065:'\\CYRSHCH', 	# character -LÉ-A
1066:'\\CYRHRDSN', 	# character -LÊ-A
1067:'\\CYRERY', 	# character -LË-A
1068:'\\CYRSFTSN', 	# character -LÌ-A
1069:'\\CYREREV', 	# character -LÍ-A
1070:'\\CYRYU', 	# character -LÎ-A
1071:'\\CYRYA', 	# character -LÏ-A
1072:'\\cyra', 	# character -LÐ-A
1073:'\\cyrb', 	# character -LÑ-A
1074:'\\cyrv', 	# character -LÒ-A
1075:'\\cyrg', 	# character -LÓ-A
1076:'\\cyrd', 	# character -LÔ-A
1077:'\\cyre', 	# character -LÕ-A
1078:'\\cyrzh', 	# character -LÖ-A
1079:'\\cyrz', 	# character -L×-A
1080:'\\cyri', 	# character -LØ-A
1081:'\\cyrishrt', 	# character -LÙ-A
1082:'\\cyrk', 	# character -LÚ-A
1083:'\\cyrl', 	# character -LÛ-A
1084:'\\cyrm', 	# character -LÜ-A
1085:'\\cyrn', 	# character -LÝ-A
1086:'\\cyro', 	# character -LÞ-A
1087:'\\cyrp', 	# character -Lß-A
1088:'\\cyrr', 	# character -Là-A
1089:'\\cyrs', 	# character -Lá-A
1090:'\\cyrt', 	# character -Lâ-A
1091:'\\cyru', 	# character -Lã-A
1092:'\\cyrf', 	# character -Lä-A
1093:'\\cyrh', 	# character -Lå-A
1094:'\\cyrc', 	# character -Læ-A
1095:'\\cyrch', 	# character -Lç-A
1096:'\\cyrsh', 	# character -Lè-A
1097:'\\cyrshch', 	# character -Lé-A
1098:'\\cyrhrdsn', 	# character -Lê-A
1099:'\\cyrery', 	# character -Lë-A
1100:'\\cyrsftsn', 	# character -Lì-A
1101:'\\cyrerev', 	# character -Lí-A
1102:'\\cyryu', 	# character -Lî-A
1103:'\\cyrya', 	# character -Lï-A
1104:'\\`\\cyre', 	# character ?
1105:'\\cyryo', 	# character -Lñ-A
1106:'\\cyrdje', 	# character -Lò-A
1107:'\\`\\cyrg', 	# character -Ló-A
1108:'\\cyrie', 	# character -Lô-A
1109:'\\cyrdze', 	# character -Lõ-A
1110:'\\cyrii', 	# character -Lö-A
1111:'\\cyryi', 	# character -L÷-A
1112:'\\cyrje', 	# character -Lø-A
1113:'\\cyrlje', 	# character -Lù-A
1114:'\\cyrnje', 	# character -Lú-A
1115:'\\cyrtshe', 	# character -Lû-A
1116:'\\`\\cyrk', 	# character -Lü-A
1117:'\\`\\cyri', 	# character ?
1118:'\\cyrushrt', 	# character -Lþ-A
1119:'\\cyrdzhe', 	# character -Lÿ-A
1122:'\\CYRYAT', 	# character ?
1123:'\\cyryat', 	# character ?
1130:'\\CYRBYUS', 	# character ?
1131:'\\cyrbyus', 	# character ?
1138:'\\CYRFITA', 	# character ?
1139:'\\cyrfita', 	# character ?
1140:'\\CYRIZH', 	# character ?
1141:'\\cyrizh', 	# character ?
1142:'\\C\\CYRIZH', 	# character ?
1143:'\\C\\cyrizh', 	# character ?
1164:'\\CYRSEMISFTSN', 	# character ?
1165:'\\cyrsemisftsn', 	# character ?
1166:'\\CYRRTICK', 	# character ?
1167:'\\cyrrtick', 	# character ?
1168:'\\CYRGUP', 	# character ?
1169:'\\cyrgup', 	# character ?
1170:'\\CYRGHCRS', 	# character ?
1171:'\\cyrghcrs', 	# character ?
1172:'\\CYRGHK', 	# character ?
1173:'\\cyrghk', 	# character ?
1174:'\\CYRZHDSC', 	# character ?
1175:'\\cyrzhdsc', 	# character ?
1176:'\\CYRZDSC', 	# character ?
1177:'\\cyrzdsc', 	# character ?
1178:'\\CYRKDSC', 	# character ?
1179:'\\cyrkdsc', 	# character ?
1180:'\\CYRKVCRS', 	# character ?
1181:'\\cyrkvcrs', 	# character ?
1182:'\\CYRKHCRS', 	# character ?
1183:'\\cyrkhcrs', 	# character ?
1184:'\\CYRKBEAK', 	# character ?
1185:'\\cyrkbeak', 	# character ?
1186:'\\CYRNDSC', 	# character ?
1187:'\\cyrndsc', 	# character ?
1188:'\\CYRNG', 	# character ?
1189:'\\cyrng', 	# character ?
1190:'\\CYRPHK', 	# character ?
1191:'\\cyrphk', 	# character ?
1192:'\\CYRABHHA', 	# character ?
1193:'\\cyrabhha', 	# character ?
1194:'\\CYRSDSC', 	# character ?
1195:'\\cyrsdsc', 	# character ?
1196:'\\CYRTDSC', 	# character ?
1197:'\\cyrtdsc', 	# character ?
1198:'\\CYRY', 	# character ?
1199:'\\cyry', 	# character ?
1200:'\\CYRYHCRS', 	# character ?
1201:'\\cyryhcrs', 	# character ?
1202:'\\CYRHDSC', 	# character ?
1203:'\\cyrhdsc', 	# character ?
1204:'\\CYRTETSE', 	# character ?
1205:'\\cyrtetse', 	# character ?
1206:'\\CYRCHRDSC', 	# character ?
1207:'\\cyrchrdsc', 	# character ?
1208:'\\CYRCHVCRS', 	# character ?
1209:'\\cyrchvcrs', 	# character ?
1210:'\\CYRSHHA', 	# character ?
1211:'\\cyrshha', 	# character ?
1212:'\\CYRABHCH', 	# character ?
1213:'\\cyrabhch', 	# character ?
1214:'\\CYRABHCHDSC', 	# character ?
1215:'\\cyrabhchdsc', 	# character ?
1216:'\\CYRpalochka', 	# character ?
1217:'\\U\\CYRZH', 	# character ?
1218:'\\U\\cyrzh', 	# character ?
1219:'\\CYRKHK', 	# character ?
1220:'\\cyrkhk', 	# character ?
1221:'\\CYRLDSC', 	# character ?
1222:'\\cyrldsc', 	# character ?
1223:'\\CYRNHK', 	# character ?
1224:'\\cyrnhk', 	# character ?
1227:'\\CYRCHLDSC', 	# character ?
1228:'\\cyrchldsc', 	# character ?
1229:'\\CYRMDSC', 	# character ?
1230:'\\cyrmdsc', 	# character ?
1232:'\\U\\CYRA', 	# character ?
1233:'\\U\\cyra', 	# character ?
1234:'\\"\\CYRA', 	# character ?
1235:'\\"\\cyra', 	# character ?
1236:'\\CYRAE', 	# character ?
1237:'\\cyrae', 	# character ?
1238:'\\U\\CYRE', 	# character ?
1239:'\\U\\cyre', 	# character ?
1240:'\\CYRSCHWA', 	# character ?
1241:'\\cyrschwa', 	# character ?
1242:'\\"\\CYRSCHWA', 	# character ?
1243:'\\"\\cyrschwa', 	# character ?
1244:'\\"\\CYRZH', 	# character ?
1245:'\\"\\cyrzh', 	# character ?
1246:'\\"\\CYRZ', 	# character ?
1247:'\\"\\cyrz', 	# character ?
1248:'\\CYRABHDZE', 	# character ?
1249:'\\cyrabhdze', 	# character ?
1250:'\\=\\CYRI', 	# character ?
1251:'\\=\\cyri', 	# character ?
1252:'\\"\\CYRI', 	# character ?
1253:'\\"\\cyri', 	# character ?
1254:'\\"\\CYRO', 	# character ?
1255:'\\"\\cyro', 	# character ?
1256:'\\CYROTLD', 	# character ?
1257:'\\cyrotld', 	# character ?
1260:'\\"\\CYREREV', 	# character ?
1261:'\\"\\cyrerev', 	# character ?
1262:'\\=\\CYRU', 	# character ?
1263:'\\=\\cyru', 	# character ?
1264:'\\"\\CYRU', 	# character ?
1265:'\\"\\cyru', 	# character ?
1266:'\\H\\CYRU', 	# character ?
1267:'\\H\\cyru', 	# character ?
1268:'\\"\\CYRCH', 	# character ?
1269:'\\"\\cyrch', 	# character ?
1270:'\\CYRGDSC', 	# character ?
1271:'\\cyrgdsc', 	# character ?
1272:'\\"\\CYRERY', 	# character ?
1273:'\\"\\cyrery', 	# character ?
1274:'\\CYRGDSCHCRS', 	# character ?
1275:'\\cyrgdschcrs', 	# character ?
1276:'\\CYRHHK', 	# character ?
1277:'\\cyrhhk', 	# character ?
1278:'\\CYRHHCRS', 	# character ?
1279:'\\cyrhhcrs', 	# character ?
3647:'\\textbaht', 	# character -Tß-A
8204:'\\textcompwordmark', 	# character ?
8211:'\\textendash', 	# character $(G!9(B
8212:'\\textemdash', 	# character $(G!7(B
8214:'\\textbardbl', 	# character $B!B(B
8216:'\\textquoteleft', 	# character -F¡-A
8217:'\\textquoteright', 	# character -F¢-A
8218:'\\quotesinglbase', 	# character ?
8220:'\\textquotedblleft', 	# character -YŽ-A
8221:'\\textquotedblright', 	# character -Y¡-A
8222:'\\quotedblbase', 	# character -Y¥-A
8224:'\\textdagger', 	# character $B"w(B
8225:'\\textdaggerdbl', 	# character $B"x(B
8226:'\\textbullet', 	# character $(0!&(B
8230:'\\textellipsis', 	# character $B!D(B
8240:'\\textperthousand', 	# character $B"s(B
8241:'\\textpertenthousand', 	# character ?
8249:'\\guilsinglleft', 	# character ?
8250:'\\guilsinglright', 	# character ?
8251:'\\textreferencemark', 	# character $B"((B
8253:'\\textinterrobang', 	# character ?
8260:'\\textfractionsolidus', 	# character $(G"_(B
8270:'\\textasteriskcentered', 	# character ?
8274:'\\textdiscount', 	# character ?
8353:'\\textcolonmonetary', 	# character ?
8356:'\\textlira', 	# character ?
8358:'\\textnaira', 	# character ?
8361:'\\textwon', 	# character ?
8363:'\\textdong', 	# character ?
8364:'\\texteuro', 	# character -b€-A
8369:'\\textpeso', 	# character ?
8451:'\\textcelsius', 	# character $B!n(B
8470:'\\textnumero', 	# character -Lð-A
8471:'\\textcircledP', 	# character ?
8478:'\\textrecipe', 	# character ?
8480:'\\textservicemark', 	# character ?
8482:'\\texttrademark', 	# character $(D"o(B
8486:'\\textohm', 	# character -FÙ-A
8487:'\\textmho', 	# character ?
8494:'\\textestimated', 	# character ?
8592:'\\textleftarrow', 	# character $B"+(B
8593:'\\textuparrow', 	# character $B",(B
8594:'\\textrightarrow', 	# character $B"*(B
8595:'\\textdownarrow', 	# character $B"-(B
9001:'\\textlangle', 	# character $B!R(B
9002:'\\textrangle', 	# character $B!S(B
9250:'\\textblank', 	# character ?
9251:'\\textvisiblespace', 	# character ?
9702:'\\textopenbullet', 	# character ?
9711:'\\textbigcircle', 	# character $B"~(B
9834:'\\textmusicalnote'	# character $B"v(B
}



def utf8tolatex(s, non_ascii_only=False, brackets=True, substitute_bad_chars=False):
    s = unicode(s); # make sure s is unicode
    s = unicodedata.normalize('NFC', s);

    if not s:
        return ""

    result = u""
    for ch in s:
        if (non_ascii_only and ord(ch) < 127):
            result += ch
        else:
            lch = utf82latex.get(ord(ch), None)
            if (lch is not None):
                # add brackets if needed, i.e. if we have a substituting macro.
                result += (  '{'+lch+'}' if brackets and lch[0] == '\\' else
                             lch  )
            else:
                logger.warning("Character cannot be encoded into LaTeX: %s" % (repr(ch)))
                if (substitute_bad_chars):
                    result += r'{\bfseries ?}'
                else:
                    # keep unescaped char
                    result += ch

    return result
    
    
