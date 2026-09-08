import os
import udapi

# Fix too-many-subjects errors in UD_Persian-Seraji (train/dev/test splits).
# 97 errors across 91 sentences.
#
# Dominant patterns:
#   1. Outer topic + inner grammatical subject → outer gets nsubj:outer
#   2. NOUN-headed temporal/locative adverbials tagged nsubj → obl
#   3. Vocative addresses tagged nsubj → vocative
#   4. Direct objects marked with را tagged nsubj → obj
#   5. Coordinated subjects where second conjunct needs conj
#   6. Quantifiers/determiners (همه, همان, دیگر) tagged as nsubj → det/appos
#   7. Miscellaneous: appos, parataxis, xcomp, advcl, reparent fixes

FIXES = {
    # ══════════════════════════════════════════════════════════════════════
    # TRAIN SPLIT
    # ══════════════════════════════════════════════════════════════════════

    # train-s128
    # TEXT:    صاحب مغازه: [در حالی که به ساعت اشاره می‌کند] ساعتم، هفت و… ساعت حدود ده دقیقه به زنگ را نشان می‌دهد.
    # TRANSLIT: ṣāḥib maġāzah: [dar ḥālī kah bah sāʿat išārah mīkonad] sāʿatam, haft wa… sāʿat ḥudūd dah daqīqah bah zang rā nišān mīdahad.
    # ENGLISH:  Shop owner: [while pointing at the clock] My watch, seven and… the watch shows about ten minutes to the bell.
    # Node 13 ساعتم (outer topic from stage direction) → nsubj:outer; node 19 ساعت (inner subject) stays nsubj
    'train-s128': [('deprel', 13, 'nsubj:outer')],

    # train-s149
    # TEXT:    دستی که یازده ساعت را پاک می‌کند و می‌نویسد: «ده ساعت به افطار مانده» احمد کیف را از روی زمین برمی‌دارد.
    # TRANSLIT: dastī kah yāzdah sāʿat rā pāk mīkonad wa mīnawīsad: «dah sāʿat bah ifṭār māndah» Aḥmad kīf rā az rūy zamīn bar mīdārad.
    # ENGLISH:  The hand that erases eleven o'clock and writes: "Ten hours until iftar" — Ahmad picks up the bag from the ground.
    # Node 1 دستی (cinematic close-up hand, outer topic) → nsubj:outer; node 18 احمد (real subject) stays nsubj
    'train-s149': [('deprel', 1, 'nsubj:outer')],

    # train-s201
    # TEXT:    زبانش را بی‌خود در دهان نمی‌چرخاند و این‌ها همه یعنی این که روزه‌دار با اراده‌ای قوی خود را کنترل می‌کند.
    # TRANSLIT: zabānash rā bīxud dar dahān namīčarxānad wa īnhā hamah yaʿnī īn kah rūzahdār bā irādahʾī qawī xud rā kontrol mīkonad.
    # ENGLISH:  He does not roll his tongue needlessly, and all of these mean that the fasting person controls himself with strong willpower.
    # Node 9 این‌ها (outer topic "all these") → nsubj:outer; node 14 روزه‌دار (inner subject) stays nsubj
    'train-s201': [('deprel', 9, 'nsubj:outer')],

    # train-s226
    # TEXT:    ببینم حسینی، تو…
    # TRANSLIT: bebīnam Ḥusaynī, to…
    # ENGLISH:  Let me see, Hosseini, you…
    # Node 2 حسینی (vocative address) → vocative; node 4 تو (real subject) stays nsubj
    'train-s226': [('deprel', 2, 'vocative')],

    # train-s247
    # TEXT:    بعضی از بچه‌ها که قبلا دیده‌ایم به هم زبان نشان می‌دهند، یک به یک سر فرو‌می‌اندازند.
    # TRANSLIT: baʿḍī az baččahā kah qablan dīdahʾīm bah ham zabān nišān mīdahand, yak bah yak sar furū mīandāzand.
    # ENGLISH:  Some of the children we have seen before show their tongues at each other, one by one they lower their heads.
    # Node 13 یک (head of fixed "یک به یک" = one by one) → obl; node 1 بعضی (real subject) stays nsubj
    'train-s247': [('deprel', 13, 'obl')],

    # train-s252
    # TEXT:    مکث روی چهره احمد، صدای زنگ روی چهره وی به گوش می‌رسد.
    # TRANSLIT: mokṯ rūy čahrah Aḥmad, ṣadāy zang rūy čahrah wī bah gūš mīrasad.
    # ENGLISH:  Pause on Ahmad's face, the sound of the bell on his face reaches the ears.
    # Node 1 مکث (cinematic stage direction, outer topic) → nsubj:outer; node 6 صدای (real subject) stays nsubj
    'train-s252': [('deprel', 1, 'nsubj:outer')],

    # train-s257
    # TEXT:    احمد تمام حواسش متوجه احمد حسینی است که تنها آن سوی خیابان در حال رفتن است.
    # TRANSLIT: Aḥmad tamām ḥawāssaš mutawajjih Aḥmad Ḥusaynī ast kah tanhā ān sūy xīyābān dar ḥāl raftan ast.
    # ENGLISH:  Ahmad — all his attention is focused on Ahmad Hosseini who is alone on the other side of the street walking away.
    # Node 1 احمد (outer topic) → nsubj:outer; node 3 حواس (inner subject "his attention") stays nsubj
    'train-s257': [('deprel', 1, 'nsubj:outer')],

    # train-s333
    # TEXT:    احمد که کمی سر برمی‌دارد، چهره‌اش برای اولین بار، از نزدیک، مادر را متوجه خود می‌کند.
    # TRANSLIT: Aḥmad kah kamī sar bar mīdārad, čahrahʾaš barāy awwalīn bār, az nazdīk, mādar rā mutawajjih xud mīkonad.
    # ENGLISH:  Ahmad who raises his head a little, his face for the first time, from close up, makes the mother notice him.
    # Node 1 احمد (outer topic) → nsubj:outer; node 7 چهره (inner subject "his face") stays nsubj
    'train-s333': [('deprel', 1, 'nsubj:outer')],

    # train-s407
    # TEXT:    وقتی کار سفارش شد، ابتدا خیلی آسان به نظر می‌آمد؛ چون چیزی که در جامعه زیاد است معضلات است، آن هم از نوع اجتماعی.
    # TRANSLIT: waqtī kār sufāriš šud, ibtidā xaylī āsān bah naẓar mīʾāmad; čun čīzī kah dar jāmiʿah ziyād ast muʿḍalāt ast, ān ham az nawʿ ijtimāʿī.
    # ENGLISH:  When the work was commissioned, it initially seemed very easy; because what is abundant in society is problems, and those too of social type.
    # Node 23 آن (appositive "those too" referring to node 20 معضلات) → appos; node 14 چیزی (real subject) stays nsubj
    'train-s407': [('deprel', 23, 'appos')],

    # train-s420
    # TEXT:    وقتی وارد این زندانها می‌شدیم... زندگیهای متفاوت و معضلات متفاوت و بدبختی‌های متفاوت، که این‌ها همه ما را به فکر وامی‌داشت که واقعا آینده چطور می‌شود.
    # TRANSLIT: waqtī wārid īn zandānhā mīšudīm… zindagīhāy mutafāwit wa muʿḍalāt mutafāwit wa badbaxtīhāy mutafāwit, kah īnhā hamah mā rā bah fikr wāmīdāšt kah wāqiʿan āyandah čiṭūr mīšawad.
    # ENGLISH:  When we entered these prisons… Different lives and different problems and different miseries, all of which made us think about what will really happen in the future.
    # Node 32 زندگیهای (fronted outer topic list) → nsubj:outer; node 43 همه (quantifier) → det of node 42 این‌ها; node 42 این‌ها stays nsubj
    'train-s420': [('deprel', 32, 'nsubj:outer'), ('deprel', 43, 'det')],

    # train-s424
    # TEXT:    ...که همه این‌ها به یک چیز برمی‌گردد: بنیان سست خانواده.
    # TRANSLIT: …kah hamah īnhā bah yak čīz bar mīgaradad: bunyān sust xānawadat.
    # ENGLISH:  …that all these trace back to one thing: the unstable foundation of the family.
    # Node 57 همه (quantifier "all") → det of node 58 این‌ها; node 58 این‌ها stays nsubj
    'train-s424': [('deprel', 57, 'det')],

    # train-s445
    # TEXT:    مشاجره و دعوا، بچه تا این‌ها را می‌بیند می‌زند بیرون…
    # TRANSLIT: mušājirih wa daʿwā, baččah tā īnhā rā mībīnad mīzanad bīrūn…
    # ENGLISH:  Quarrel and fight — as soon as the child sees these, [the child] runs away…
    # Node 1 مشاجره (fronted outer topic) → nsubj:outer; node 5 بچه (real subject) stays nsubj
    'train-s445': [('deprel', 1, 'nsubj:outer')],

    # train-s455
    # TEXT:    من به عنوان تهیه‌کننده و کارگردان ۲۶ قسمت اول، باید بگویم، تحصیلاتی که دارم هنری است و در مورد معضلات اجتماعی فقط می‌توانم به دیده‌ها و تجربه‌هایم اکتفا کنم.
    # TRANSLIT: man bah ʿunwān tahiyyahkonandah wa kārgardān 26 qismat awwal, bāyad begūyam, taḥṣīlātī kah dāram hunarī ast…
    # ENGLISH:  I, as producer and director of the first 26 episodes, must say: the education I have is in the arts…
    # Node 14 تحصیلاتی (outer topic of embedded content clause) → nsubj:outer; node 1 من (real matrix subject) stays nsubj
    'train-s455': [('deprel', 14, 'nsubj:outer')],

    # train-s459
    # TEXT:    شما هم هر چیزی که از دانشگاه، کالج و یا از توی کتاب و هر جای دیگر در‌آوردید، مثل مرجع از آن استفاده کنید.
    # TRANSLIT: šomā ham har čīzī kah az dānišgāh, kālij wa yā az tūy kitāb wa har jāy dīgar darāwardīd, misl marjaʿ az ān istifādah konīd.
    # ENGLISH:  You too, whatever you got from university, college, or from inside books, use it as a reference.
    # Node 4 چیزی (topicalized object with resumptive pronoun آن) → obj; node 1 شما (real subject) stays nsubj
    'train-s459': [('deprel', 4, 'obj')],

    # train-s475
    # TEXT:    وقتی کارشناس گروه می‌گوید مردی که با زنش می‌نشست و تریاک می‌کشید...
    # TRANSLIT: waqtī kāršenās gorūh mīgūyad mardī kah bā zannaš mīnišast wa taryāk mīkašīd…
    # ENGLISH:  When the group expert says [about] a man who used to sit with his wife and smoke opium…
    # Node 5 مردی (outer topic of reported speech) → nsubj:outer; node 2 کارشناس (real speaker subject) stays nsubj
    'train-s475': [('deprel', 5, 'nsubj:outer')],

    # train-s503
    # TEXT:    این همان چیزی است که ما توی برنامه‌های معقول اجتماعی می‌بینیم کارشناسی می‌آید و حکم می‌دهد.
    # TRANSLIT: īn hamān čīzī ast kah mā tūy barnāmahāy maʿqūl ijtimāʿī mībīnīm kāršenāsī mīāyad wa ḥokm mīdahad.
    # ENGLISH:  This is the very thing we see in sensible social programs — an expert comes and passes judgment.
    # Node 2 همان (DET intensifier "same/very") → det of node 3 چیزی; node 1 این (real subject) stays nsubj
    'train-s503': [('deprel', 2, 'det')],

    # train-s530
    # TEXT:    هر هفته تقریبا در هر موردی که برنامه پخش می‌شود ما تلفن داریم.
    # TRANSLIT: har haftah taqrīban dar har mawridī kah barnāmah paxš mīšawad mā tilefon dārīm.
    # ENGLISH:  Every week, approximately, for every topic the program broadcasts on, we have phone calls.
    # Node 2 هفته (temporal frame "every week", NOUN head → obl); node 11 ما (real subject) stays nsubj
    'train-s530': [('deprel', 2, 'obl')],

    # train-s547
    # TEXT:    آقای عقیلی، آقای رایانی، در این برنامه یک بخشی دارید به عنوان بخش گفت و گو با هنرمندان.
    # TRANSLIT: āqāy ʿAqīlī, āqāy Rāyānī, dar īn barnāmah yak baxšī dārīd bah ʿunwān baxš goft wa gū bā hunarmandān.
    # ENGLISH:  Mr. Aghili, Mr. Rayani, in this program you have a section called dialogue with artists.
    # Node 1 آقای (vocative address) → vocative; node 11 بخشی (object "a section" of "have") → obj
    'train-s547': [('deprel', 1, 'vocative'), ('deprel', 11, 'obj')],

    # train-s548
    # TEXT:    زمانی که من این بخش را دیدم احساس جالبی داشتم.
    # TRANSLIT: zamānī kah man īn baxš rā dīdam iḥsās jālebī dāštam.
    # ENGLISH:  When I saw this section, I had an interesting feeling.
    # Node 1 زمانی (temporal clause head "when I saw this section", NOUN head → obl); node 8 احساس (real subject) stays nsubj
    'train-s548': [('deprel', 1, 'obl')],

    # train-s553
    # TEXT:    برنامه ما حتی مجری هم ندارد.
    # TRANSLIT: barnāmah mā ḥattā mojrī ham nadārad.
    # ENGLISH:  Our program doesn't even have a host.
    # Node 4 مجری (object of "doesn't have") → obj; node 1 برنامه (real subject) stays nsubj
    'train-s553': [('deprel', 4, 'obj')],

    # train-s558
    # TEXT:    شما می‌دانید هنرمندان ما عموما گرفتارند و هماهنگی با این‌ها و حضورشان در یک مقطع زمانی خاص در برنامه یک مقدار برای ما مشکل بود.
    # TRANSLIT: šomā mīdānīd hunarmandān mā ʿumūman giriftārand wa hamāhangī bā īnhā wa ḥużūršān dar yak maqṭaʿ zamānī xāṣ dar barnāmah yak meqdār barāy mā moškel būd.
    # ENGLISH:  You know our artists are generally busy and coordinating with them and their attendance at a specific time in the program was somewhat difficult for us.
    # Node 23 مقدار (degree modifier "somewhat", NOUN head → obl); node 9 هماهنگی (real subject) stays nsubj
    'train-s558': [('deprel', 23, 'obl')],

    # train-s564
    # TEXT:    یکی از مشکلاتی که ما داشتیم در دعوت از عزیزان - حالا من از ایشان ایراد نمی‌گیرم - و این به خاطر برخورد بد برنامه‌سازهاست، این است که...
    # TRANSLIT: yakī az moškılātī kah mā dāštīm dar daʿwat az ʿazīzān - ḥālā man az īšān īrād namīgiram - wa īn bah xāṭir barxord bad barnāmasāzahāst, īn ast kah…
    # ENGLISH:  One of the problems we had in inviting the dear guests — now I don't criticize them — and this is because of the bad behavior of program-makers, this is that…
    # Node 1 یکی (outer topic "one of the problems") → nsubj:outer; node 13 من (subject of parenthetical) stays nsubj
    'train-s564': [('deprel', 1, 'nsubj:outer')],

    # train-s574
    # TEXT:    شما در طراحی صحنه پلاتو، یک در زندان گذاشته بودید که بافت فلز رویش خورده بود و درواقع گل‌میخ بود.
    # TRANSLIT: šomā dar ṭarāḥī ṣaḥnah pelātū, yak dar zandān gozāšta būdīd kah bāft felezz rūyaš xordah būd wa darwāqeʿ golmīx būd.
    # ENGLISH:  You, in the set design, had placed a prison door on which the metal texture had worn and it was actually a rivet.
    # Node 8 در (a prison door, object of گذاشته بودید) → obj; node 1 شما (real subject) stays nsubj
    'train-s574': [('deprel', 8, 'obj')],

    # train-s584
    # TEXT:    درست جایگاهی که انسان باید در آنجا باشد؛ یعنی من خواستم این تضاد دربیاید.
    # TRANSLIT: dorost jāygāhī kah insān bāyad dar ānjā bāšad; yaʿnī man xāstam īn tażādd dar biyāyad.
    # ENGLISH:  Exactly the position that a human being should be in; meaning I wanted this contrast to emerge.
    # Node 2 جایگاهی (outer topic from first clause) → nsubj:outer; node 11 من (real subject of second clause) stays nsubj
    'train-s584': [('deprel', 2, 'nsubj:outer')],

    # train-s598
    # TEXT:    یک جاهایی وله‌ها عالی بود، بخصوص در قسمتهای سری اول که وله‌ها مخاطب را با یک کار متفاوت روبه‌رو می‌کرد.
    # TRANSLIT: yak jāhāyī walahā ʿālī būd, baxuṣūṣ dar qismatāy sarī awwal kah walahā moxāṭab rā bā yak kār mutafāwit rūbahrū mīkard.
    # ENGLISH:  In some places the jingles were excellent, especially in the episodes of the first series where the jingles confronted the audience with a different work.
    # Node 2 جاهایی (locative frame "in some places", NOUN head → obl); node 3 وله‌ها (real subject) stays nsubj
    'train-s598': [('deprel', 2, 'obl')],

    # train-s607
    # TEXT:    اما در مونتاژ بیشترین ضرر را دادیم؛ یعنی شاید بتوانم بگویم مونتاژ این برنامه هر قسمتش حدود سیصد هزار تومان برای ما تمام شد.
    # TRANSLIT: ammā dar montāž bīšterīn żarar rā dādīm; yaʿnī šāyad betawānam begūyam montāž īn barnāmah har qismataš ḥodūd sīṣad hezār tomān barāy mā tamām šod.
    # ENGLISH:  But in editing we suffered the most loss; I might say the editing of each episode of this program cost us about 300 thousand tomans.
    # Node 13 مونتاژ (outer topic "editing of this program") → nsubj:outer; node 17 قسمت (inner subject "each episode") stays nsubj
    'train-s607': [('deprel', 13, 'nsubj:outer')],

    # train-s655
    # TEXT:    آقای باقری به عنوان بازبین و آقای مأمنی این‌ها همه کمک کردند.
    # TRANSLIT: āqāy Bāqirī bah ʿunwān bāzbīn wa āqāy Maʾmanī īnhā hamah komak kardand.
    # ENGLISH:  Mr. Bagheri as reviewer and Mr. Mameni — all of these helped.
    # Node 1 آقای (outer topic: named persons as outer list) → nsubj:outer; node 10 همه (quantifier "all") → det of node 9 این‌ها; node 9 این‌ها (resumptive, real subject) stays nsubj
    'train-s655': [('deprel', 1, 'nsubj:outer'), ('deprel', 10, 'det')],

    # train-s663
    # TEXT:    بیشترین برآوردها در مورد تماشاگران از نظرسنجی‌های عادی به دست آمده است؛ زمانی که هیچ کنترل مستقلی وجود نداشته است.
    # TRANSLIT: bīšterīn barāwardha dar mawrid tamāšāgarān az naẓarsanjīhāy ʿādī bah dast āmadah ast; zamānī kah hīč kontrol mostaqellī wujūd nadāšta ast.
    # ENGLISH:  Most estimates about viewers come from ordinary polls; at a time when there was no independent control.
    # Node 14 زمانی (temporal adverbial clause head, NOUN head → obl); node 2 برآوردها (real subject) stays nsubj
    'train-s663': [('deprel', 14, 'obl')],

    # train-s689
    # TEXT:    بدین ترتیب، گروه سوم بینندگان برنامه‌های مذهبی «جویندگان کنجکاو» معرفی شدند.
    # TRANSLIT: badīn tartīb, gorūh sowwom bīnandagān barnāmahāy mazhabī «jūyandagān konjkāw» moʿarrafī šodand.
    # ENGLISH:  In this way, the third group of viewers of religious programs, "curious seekers," were introduced.
    # Node 7 بینندگان (viewers, should modify گروه not be sister nsubj) → reparent to node 5 گروه, deprel nmod:poss
    'train-s689': [('reparent', 7, 5, 'nmod:poss')],

    # train-s699
    # TEXT:    برنامه‌های مذهبی صبح یکشنبه بیننده بسیار کمی دارند؛ چیزی حدود چهار صد هزار تا ششصد هزار بیننده.
    # TRANSLIT: barnāmahāy mazhabī ṣobḥ yakšambah bīnandah besyār kamī dārand; čīzī ḥodūd čahār ṣad hezār tā šeṣad hezār bīnandah.
    # ENGLISH:  Sunday morning religious programs have very few viewers; something around 400–600 thousand viewers.
    # Node 5 بیننده (object "viewer" of "have") → obj; node 1 برنامه‌های (real subject) stays nsubj
    'train-s699': [('deprel', 5, 'obj')],

    # train-s727
    # TEXT:    بنابراین با توجه به رویکرد جدید به مذهب در سطوح مختلف، صاحب‌نظران علوم اجتماعی و رفتاری، بخصوص متخصصان بهداشت روانی، به رسانه‌ها و مخاطبان آن توصیه می‌کنند که مذهب را رکن اصلی فعالیتهای خود قرار دهند.
    # TRANSLIT: banābirayn bā tawajjoh bah rūykard jadīd bah mazhab dar sṭūḥ moxtalef, ṣāḥibnażarān ʿolūm ijtimāʿī wa raftārī, baxuṣūṣ motaxaṣṣeṣān behdāšt rawānī, bah resānehā wa moxāṭabān ān tawṣīya mīkonand…
    # ENGLISH:  Therefore, social and behavioral science experts, especially mental health specialists, recommend to the media and their audiences to make religion the cornerstone of their activities.
    # Node 20 متخصصان (second coordinated subject "specialists") → conj of node 13 صاحب‌نظران; node 13 stays nsubj
    'train-s727': [('deprel', 20, 'conj')],

    # train-s748
    # TEXT:    ۹ - آگهی‌های رادیویی - تلویزیونی که بند ۳ / ۱۰ آن‌ها را مجاز بداند، می‌توانند نشریات مجانی برای تماشاگران ارسال دارند.
    # TRANSLIT: 9 - āgehīhāy rādīūyī - televīzīūnī kah band 3/10 ānhā rā mojāz bedānad, mītawānand nošrīyāt majjānī barāy tamāšāgarān arsāl dārand.
    # ENGLISH:  9 - Radio-TV ads that article 3/10 permits may send free publications to viewers.
    # Node 18 نشریات (free publications, object of "may send") → obj; node 3 آگهی‌های (real subject) stays nsubj
    'train-s748': [('deprel', 18, 'obj')],

    # train-s754
    # TEXT:    ۱۴ - بریتانیا جوامع گوناگونی را با باورها و فرهنگ‌های مختلف در بر دارد و هر یک دارای حساسیت‌های دینی خاص خویش هستند.
    # TRANSLIT: 14 - Brīṭānyā jawāmeʿ gonāgūnī rā bā bāwarhā wa farhangāy moxtalef dar bar dārad wa har yak dārāy ḥasāssīyatāy dīnī xāṣ xwīš hastand.
    # ENGLISH:  14 - Britain contains diverse communities with various beliefs and cultures and each one has their own specific religious sensitivities.
    # Node 19 حساسیت‌های (object of دارای "having sensitivities") → reparent to node 18 دارای, deprel obj; node 17 یک (real subject "each one") stays nsubj
    'train-s754': [('reparent', 19, 18, 'obj')],

    # train-s778
    # TEXT:    اتفاقی که در سری قبل افتاد و باعث شد سریال خیلی تماشاگر پیدا کند همین ملودرام بودنش بود، یعنی ما بیشتر طرف این می‌رفتیم که در احساسات تماشاگر هم تأثیر بگذاریم و هم بخندانیم و هم بگریانیم.
    # TRANSLIT: ettifāqī kah dar sarī qabl oftād wa bāʿeṯ šod sarīyāl xaylī tamāšāgar pīdā konad hamīn melodrām bodanaš būd, yaʿnī mā bīštar ṭaraf īn mīraftīm kah…
    # ENGLISH:  The event that happened in the previous series and caused the serial to gain many viewers was this melodrama quality, meaning we went more toward affecting the viewer's emotions.
    # Node 1 اتفاقی (outer topic "the event that happened") → nsubj:outer; node 22 ما (real subject) stays nsubj
    'train-s778': [('deprel', 1, 'nsubj:outer')],

    # train-s779
    # TEXT:    این دفعه من سعی کردم همه توانم را روی سوژه‌ها بگذارم و یک نگاه تازه اجتماعی داشته باشم.
    # TRANSLIT: īn dafʿah man saʿī kardam hamah tawānam rā rūy sūžehā begozāram wa yak negāh tāzah ijtimāʿī dāšta bāšam.
    # ENGLISH:  This time I tried to put all my ability into the subjects and have a fresh social perspective.
    # Node 2 دفعه (temporal frame "this time", NOUN head → obl); node 3 من (real subject) stays nsubj
    'train-s779': [('deprel', 2, 'obl')],

    # train-s805
    # TEXT:    اخلاقیات خاصی هست که هر لهجه‌ای آن را بروز می‌دهد؛ مثلا در «روزگار جوانی» می‌دیدیم که شخصیت احد... یک جاهایی ساده و دیر‌فهم می‌شد.
    # TRANSLIT: axlāqīyāt xāṣī hast kah har lahje'ī ān rā borūz mīdahad; masalan dar «Rūzgār-e Javānī» mīdīdīm kah šaxṣīyyat Aḥad… yak jāhāyī sādah wa dīrfahm mīšod.
    # ENGLISH:  There are specific ethics that each dialect expresses; for example in Roozgar-e Javani we saw that the character of Ahmad in some places became simple and slow-to-understand.
    # Node 30 جاهایی (locative frame "in some places", NOUN head → obl); node 20 شخصیت (subject) stays nsubj
    'train-s805': [('deprel', 30, 'obl')],

    # train-s814
    # TEXT:    ولی آن درصد زرنگشان، چون خیلی از آن‌ها آمدند تهران و رفتند به شهرهای دیگر، مردم شهرهای دیگر اصفهانی‌ها را از روی این تعداد می‌شناسند.
    # TRANSLIT: wallī ān deraṣad zorrangšān, čon xaylī az ānhā āmadand Tehrān wa raftand bah šahrhāy dīgar, mardom šahrhāy dīgar Eṣfahānīhā rā az rūy īn taʿdād mīšenāsand.
    # ENGLISH:  But that clever percentage of them, because many of them came to Tehran and went to other cities, people from other cities recognize Isfahanis by this number.
    # Node 3 درصد (outer topic "that percentage of them") → nsubj:outer; node 8 خیلی (real subject of advcl) stays nsubj
    'train-s814': [('deprel', 3, 'nsubj:outer')],

    # train-s821
    # TEXT:    یادم است هفت - هشت قسمت آن کار که رفت، یک نگرانی به ما دست داد که این بچه‌ها با بچه‌های «روزگار جوانی» مقایسه می‌شدند.
    # TRANSLIT: yādam ast haft - hašt qismat ān kār kah raft, yak negarānī bah mā dast dād kah īn baččahā bā baččahāy «Rūzgār-e Javānī» moqāyasah mīšodand.
    # ENGLISH:  I remember that after seven-eight episodes of that work aired, a worry came to us that these children were being compared with children of Roozgar-e Javani.
    # Node 6 قسمت (temporal frame "seven-eight episodes", NOUN head → obl); node 13 نگرانی (real subject) stays nsubj
    'train-s821': [('deprel', 6, 'obl')],

    # train-s845
    # TEXT:    این چرا راه اشتباهی است؟
    # TRANSLIT: īn čarā rāh eštebāhī ast?
    # ENGLISH:  Why is this the wrong way?
    # Node 1 این (demonstrative pronoun modifying راه "this way") → reparent to node 3 راه, deprel det; node 3 راه stays nsubj
    'train-s845': [('reparent', 1, 3, 'det')],

    # train-s850
    # TEXT:    پس من نباید آن‌ها را می‌آوردم، یک جور نارو زدن به تماشاگر بود، اگر من همان آدمها را می‌آوردم، چون داستان آن‌ها تمام شده بود.
    # TRANSLIT: pas man nabāyad ānhā rā mīāwardam, yak jūr nārū zadan bah tamāšāgar būd, agar man hamān ādamhā rā mīāwardam, čon dāstān ānhā tamām šodah būd.
    # ENGLISH:  So I shouldn't have brought them — it was a kind of cheating the viewer, if I had brought the same people, since their story had ended.
    # Node 11 زدن (head of paratactic clause "was a kind of cheating") → parataxis; node 2 من (real subject of ROOT) stays nsubj
    'train-s850': [('deprel', 11, 'parataxis')],

    # train-s851
    # TEXT:    تصور کن که اگر ما مثلا بعد از این که مونس و رفیع دیگر قضیه‌شان حل شد و به جایی نرسیدند، می‌خواستیم داستان را ادامه بدهیم، باید یک داستان جدید برای رفیع می‌ساختیم.
    # TRANSLIT: taṣawwar kon kah agar mā masalan baʿd az īn kah Mūnes wa Rafīʿ dīgar qażīyahšān ḥall šod wa bah jāyī naresīdand, mīxāstīm dāstān rā edāmah bedahīm, bāyad yak dāstān jadīd barāy Rafīʿ mīsāxtīm.
    # ENGLISH:  Imagine that if we, after Moones and Rafi's matter was resolved and they hadn't reached anywhere, had wanted to continue the story, we would have had to create a new story for Rafi.
    # Node 5 ما (subject of main clause "we wanted") → reparent to node 28 بدهیم, deprel nsubj; node 11 مونس (subject of conditional advcl) stays nsubj
    'train-s851': [('reparent', 5, 28, 'nsubj')],

    # train-s880
    # TEXT:    یک قسمت اصلا سروش صحت به چشم نمی‌آید و سعید آقاخانی برجسته‌تر می‌شود، و برعکس.
    # TRANSLIT: yak qismat aṣlan Sorūš Ṣeḥḥat bah češm namīāyad wa Saʿīd Āqāxānī barjastetār mīšawad, wa barʿaks.
    # ENGLISH:  In one episode Sorush Sahat doesn't appear at all and Saeed Aghakhani stands out more, and vice versa.
    # Node 2 قسمت (temporal frame "one episode", NOUN head → obl); node 4 سروش (real subject) stays nsubj
    'train-s880': [('deprel', 2, 'obl')],

    # train-s900
    # TEXT:    سوم این که این آدم اگرچه فیلمهای دفاع مقدس خیلی بازی کرده بود، ولی در این تیپ کلیشه نبود.
    # TRANSLIT: sowwom īn kah īn ādam agarčah filmmāy defāʿ moqaddas xaylī bāzī kardah būd, wallī dar īn tayyep klīšeh nabūd.
    # ENGLISH:  Third: this person, although he had acted a lot in holy defense films, was not a cliché in this role.
    # Node 2 این (outer clausal topic "this fact that…") → nsubj:outer; node 5 آدم (inner subject) stays nsubj
    'train-s900': [('deprel', 2, 'nsubj:outer')],

    # train-s905
    # TEXT:    نه، به خاطر این است که ایرانمنش در واقع یک کارهایی در شخصیتش انجام می‌دهد.
    # TRANSLIT: nah, bah xāṭir īn ast kah Īrānmanš dar wāqeʿ yak kārhāyī dar šaxṣīyyataš anjām mīdahad.
    # ENGLISH:  No, the reason is that Iranmanesh actually does certain things in his character.
    # Node 12 کارهایی (object "certain things") → obj; node 8 ایرانمنش (real subject) stays nsubj
    'train-s905': [('deprel', 12, 'obj')],

    # train-s934
    # TEXT:    ولی آن نیمایی که من در فیلم می‌دیدم، باید موهایش خیلی بلند و خشک باشد.
    # TRANSLIT: wallī ān Nīmāyī kah man dar film mīdīdam, bāyad mūhāyaš xaylī boland wa xošk bāšad.
    # ENGLISH:  But that Nimayi I saw in the film — his hair should be very long and dry.
    # Node 3 نیمایی (outer topic "that Nimayi character") → nsubj:outer; node 11 موهای (inner subject "his hair") stays nsubj
    'train-s934': [('deprel', 3, 'nsubj:outer')],

    # train-s945
    # TEXT:    شاید من این حس را ندارم و احساس می‌کنم در این بچه‌ها کسی که خوب در آمده، نیما رئی‌س است و یک‌جوری هم سعید، بقیه هنوز در نیامده‌اند.
    # TRANSLIT: šāyad man īn ḥess rā nadāram wa eḥsās mīkonam dar īn baččahā kasī kah xub dar āmadah, Nīmā Raʾīs ast wa yakjūrī ham Saʿīd, baqīyah hanūz dar nayāmadahānd.
    # ENGLISH:  Maybe I don't have this sense, and I feel that among these children the one who came out well is Nima Raees, and in a way Saeed too, the rest haven't come out yet.
    # Node 25 سعید (conjoined second predicate nominal "Saeed too") → conj of node 19 نیما; node 13 کسی (real subject) stays nsubj
    'train-s945': [('deprel', 25, 'conj')],

    # train-s947
    # TEXT:    ولی مطمئنم که آدم برجسته، این کار نیما رئی‌س است؛ و باز هنوز نمی‌توانم بگویم چی می‌شود.
    # TRANSLIT: wallī moṭmaʾennam kah ādam barjastah, īn kār Nīmā Raʾīs ast; wa bāz hanūz namītawānam begūyam čī mīšawad.
    # ENGLISH:  But I'm certain that the outstanding person — this work — is Nima Raees; and I still can't say what will happen.
    # Node 5 آدم (outer topic "the outstanding person") → nsubj:outer; node 9 کار (inner subject "this work") stays nsubj
    'train-s947': [('deprel', 5, 'nsubj:outer')],

    # train-s977
    # TEXT:    همه این‌ها خیلی خوب بود، تا آخر تماشاگر را می‌گرفت.
    # TRANSLIT: hamah īnhā xaylī xub būd, tā āxar tamāšāgar rā mīgraft.
    # ENGLISH:  All of these were very good, it held the viewer's attention to the end.
    # Node 1 همه (quantifier "all") → det of node 2 این‌ها; node 2 این‌ها (real subject) stays nsubj
    'train-s977': [('deprel', 1, 'det')],

    # train-s990
    # TEXT:    این قصه اگر در یک سریال دیگری بود... قشنگی این سوژه یک حرف بود؛ چیزی که سالها و مدتهاست در ذهن ماست.
    # TRANSLIT: īn qeṣṣah agar dar yak sarīyāl dīgarī būd… qošangī īn sūžah yak ḥarf būd; čīzī kah sālhā wa moddathāst dar zehn māst.
    # ENGLISH:  …the beauty of this subject was a word — something that has been in our minds for years.
    # Node 39 چیزی (appositive elaborating on node 36 حرف "a word") → appos of node 36; node 32 قشنگی (real subject) stays nsubj
    'train-s990': [('deprel', 39, 'appos')],

    # train-s999
    # TEXT:    این که این پیرمرد قهوه‌چی است و هیچ چیز نمی‌داند و جگر خرد می‌کند و یک بچه هم دارد، خوب می‌داند عشق یعنی چه.
    # TRANSLIT: īn kah īn pīrmard qahwečī ast wa hīč čīz namīdānad wa jegar xord mīkonad wa yak baččah ham dārad, xub mīdānad ʿešq yaʿnī čah.
    # ENGLISH:  The fact that this old coffee-house keeper is what he is and knows nothing… he well knows what love means.
    # Node 1 این (outer clausal topic "the fact that…") → nsubj:outer; node 4 پیرمرد (inner subject) stays nsubj
    'train-s999': [('deprel', 1, 'nsubj:outer')],

    # train-s1063
    # TEXT:    همیشه در سریالها پدرها مثبت بوده‌اند و پسرها خام و نپخته.
    # TRANSLIT: hamīšah dar sarīyālhā pedarhā moṯbet bodahānd wa pesarhā xām wa napoxta.
    # ENGLISH:  Always in serials fathers have been positive and sons raw and unrefined.
    # Node 8 پسرها (coordinated subject "sons") → conj of node 4 پدرها; node 4 stays nsubj
    'train-s1063': [('deprel', 8, 'conj')],

    # train-s1108
    # TEXT:    اتفاقی که در آن سری افتاد، این بود که این آدم یک سری چیزهایش - مثلا، این آدم از قسمت اول تا پانزدهم با خودش حرف می‌زد؛ از پانزدهم تا هجدهم خیلی کم، و از هجدهم به بعد اصلا این کار را نمی‌کرد.
    # TRANSLIT: ettifāqī kah dar ān sarī oftād, īn būd kah īn ādam yak sarī čīzhāyaš - masalan, īn ādam az qismat awwal tā pānzdahom bā xodaš ḥarf mīzad; az pānzdahom tā hijdahom xaylī kam, wa az hijdahom bah baʿd aṣlan īn kār rā namīkard.
    # ENGLISH:  The event that happened in that series was that this person's various things — for example, this person from episode 1 to 15 used to talk to himself; from 15 to 18 very little, and after 18 not at all.
    # Node 12 آدم (first mention, real subject) stays nsubj; node 21 آدم (second parenthetical/resumptive mention) → nsubj:outer
    'train-s1108': [('deprel', 21, 'nsubj:outer')],

    # train-s1288
    # TEXT:    روزنامه ابرار با عنوان "قوه قضائیه و بلاتکلیفی مطبوعات توقیف‌شده" نوشته است: اظهارات سخنگوی قوه قضائیه در خصوص سرنوشت روزنامه‌های توقیف‌شده و تعامل آتی محاکم قضایی با دست‌اندرکاران آن‌ها، راه را برای اظهارنظرهای متعدد هموار ساخت.
    # TRANSLIT: rūznāmah Abrār bā ʿonwān "quwwah qażāʾīyyah wa belātaklīfī maṭbūʿāt towqīfšodah" nevešta ast: eẓhārāt soxangūy quwwah qażāʾīyyah dar xoṣūṣ sarnewešt rūznāmahāy towqīfšodah wa taʿāmol āyandah maḥākem qażāʾī bā dastandardakārān ānhā, rāh rā barāy eẓhārnaẓarhāy motaʿadded hamwār sāxt.
    # ENGLISH:  The Abrar newspaper under the headline "Judiciary and the limbo of seized publications" has written: the statements of the judiciary spokesperson regarding the fate of seized newspapers and future court interactions paved the way for numerous opinions.
    # Node 1 روزنامه (outer topic "the Abrar newspaper") → nsubj:outer; node 16 اظهارات (inner subject "statements") stays nsubj
    'train-s1288': [('deprel', 1, 'nsubj:outer')],

    # train-s1324
    # TEXT:    ما همه می‌آییم و می‌رویم و ان‌شاأالله نظام و انقلاب باقی می‌ماند.
    # TRANSLIT: mā hamah mīāyīm wa mīrawīm wa inšāʾallāh neẓām wa enqelāb bāqī mīmānad.
    # ENGLISH:  We all come and go, and God willing the system and the revolution will remain.
    # Node 2 همه (quantifier "all", appositive of ما) → appos of node 1 ما; node 1 ما stays nsubj
    'train-s1324': [('deprel', 2, 'appos')],

    # train-s1371
    # TEXT:    ما دیگر حوصله‌مان سر رفت.
    # TRANSLIT: mā dīgar ḥawṣelamān sar raft.
    # ENGLISH:  We have run out of patience (lit. our patience has gone to its head).
    # Node 1 ما (outer topic possessor "we/our") → nsubj:outer; node 3 حوصله (inner subject "patience") stays nsubj
    'train-s1371': [('deprel', 1, 'nsubj:outer')],

    # train-s1462
    # TEXT:    مروان گفت: شما ای بنی‌هاشم بر ما ستم کردید.
    # TRANSLIT: Marwān goft: šomā ay Banīhāšem bar mā setam kardīd.
    # ENGLISH:  Marwan said: You, O Banu Hashim, have oppressed us.
    # Node 6 بنی‌هاشم (vocative address in "ای بنی‌هاشم") → vocative; node 4 شما (real subject) stays nsubj
    'train-s1462': [('deprel', 6, 'vocative')],

    # train-s1501
    # TEXT:    مهر و داغ در موزه بابل همزمان با روز جهانی موزه و هفته میراث فرهنگی، نمایشگاهی از ۳۰ نمونه مهر و داغ در موزه بابل برگزار می‌شود.
    # TRANSLIT: Mohr wa Dāġ dar Mūzah Bābol hamzamān bā Rūz Jahānī Mūzah wa Haftah Mīrāṯ Farhangi, namāyešgāhī az 30 nemūnah mohr wa dāġ dar Mūzah Bābol bargozār mīšawad.
    # ENGLISH:  "Stamp and brand at Babylon Museum" — coinciding with World Museum Day and Cultural Heritage Week, an exhibition of 30 specimens is being held.
    # Node 1 مهر (outer topic, headline-style title phrase) → nsubj:outer; node 17 نمایشگاهی (real subject) stays nsubj
    'train-s1501': [('deprel', 1, 'nsubj:outer')],

    # train-s1502
    # TEXT:    به گزارش روابط عمومی سازمان میراث فرهنگی کشور، مهر خرمن و داغ که دو نمونه از اشیاء موزه‌ای مردم‌شناسی است، هر دو از نشانه‌های مالکیت در زندگی مبتنی بر تولید کشاورزی و دامداری است.
    # TRANSLIT: bah gozāreš rawābeṭ ʿomūmī sāzmān mīrāṯ farhangī kešwar, Mohr Xarman wa Dāġ kah do nemūnah az ašyāʾ mūzahʾī mardomšenāsī ast, har do az nešānahāy mālikīyyat dar zandagī mobtanī bar towlīd kešāwarzī wa dāmdārī ast.
    # ENGLISH:  According to the Cultural Heritage Organization's PR, the mhr-kherman and dag, which are two ethnographic museum specimens, are both among signs of ownership in agricultural and livestock-based life.
    # Node 10 مهر (outer topic NP with relative clause) → nsubj:outer; node 24 دو (inner subject "both") stays nsubj
    'train-s1502': [('deprel', 10, 'nsubj:outer')],

    # train-s1613
    # TEXT:    این زندان تحت تدابیر شدید امنیتی اداره می‌شود و به‌شدت در کنترل پلیس و مقامات امنیتی است، اما مقامات و مأموران هیچ یک متوجه نشدند که زندانیان مدتی طولانی وقت صرف کردند تا تونل را حفر و سپس نقشه فرار خود را عملی کنند.
    # TRANSLIT: īn zandān taḥt tadābīr šadīd amnīyyatī edārah mīšawad wa bah šeddat dar kontrol polīs wa maqāmāt amnīyyatī ast, ammā maqāmāt wa maʾmūrān hīč yak motawajjeh našodand kah zandānīyān moddatī ṭawlānī waqt ṣarf kardand…
    # ENGLISH:  This prison is managed under strict security measures… but officials and agents — not a single one noticed that the prisoners spent a long time digging a tunnel.
    # Node 20 مقامات (outer topic, conjoined list) → nsubj:outer; node 24 یک (هیچ یک "not one", real subject) stays nsubj
    'train-s1613': [('deprel', 20, 'nsubj:outer')],

    # train-s1618
    # TEXT:    افرادی که تمبرهای شخصی سفارش دادند همگی کسانی بودند که میل داشتند طرف مکاتبه خود را غافلگیر کنند.
    # TRANSLIT: afrādī kah tambarhāy šaxṣī sefāreš dādand hamgī kasānī bodand kah meyl dāštand ṭaraf mokātabah xod rā ġāfelgīr konand.
    # ENGLISH:  All of those who ordered personal stamps were people who wanted to surprise their correspondents.
    # Node 1 افرادی (outer topic with relative clause "people who ordered…") → nsubj:outer; node 7 همگی (inner subject "all of them") stays nsubj
    'train-s1618': [('deprel', 1, 'nsubj:outer')],

    # train-s1946
    # TEXT:    آقای بهزاد نبوی می‌گوید: بخشی از مخالفان آقای خاتمی می‌گویند حاکمیت از آن خدا است و نماینده خدا هم ما هستیم و بقیه نمی‌فهمند.
    # TRANSLIT: āqāy Behzād Nabawī mīgūyad: baxšī az moxāleān āqāy Xātamī mīgūyand ḥākemīyyat az ān Xodā ast wa namāyandeye Xodā ham mā hastīm wa baqīyah namīfahmand.
    # ENGLISH:  Mr. Behzad Nabavi says: some of the opponents of Mr. Khatami say that sovereignty belongs to God and we are the representatives of God, and the rest don't understand.
    # Node 6 بخشی (real subject of می‌گویند) stays nsubj; node 12 حاکمیت (subject of copular clause inside reported speech) → nsubj:outer
    'train-s1946': [('deprel', 12, 'nsubj:outer')],

    # train-s2083
    # TEXT:    امام حسین) ع (گفت: بدهی‌ات بر عهدهٔ من.
    # TRANSLIT: Emām Ḥosayn (ʿalayh al-salām) goft: bedahīyāt bar ʿohdahye man.
    # ENGLISH:  Imam Husayn (peace be upon him) said: Your debt is upon me.
    # Node 1 امام (real speaker subject of گفت) stays nsubj; node 8 بدهی‌ات (subject of reported copular clause) → nsubj:outer
    'train-s2083': [('deprel', 8, 'nsubj:outer')],

    # train-s2108
    # TEXT:    کینه‌ای کهنه، در جنگ احد وقتی پیکر پاک حمزه سیدالشهداأ بر خاک افتاده بود، همسر ابوسفیان، هند گفت: شکم حمزه را پاره پاره کردند و جگرش را بیرون آوردند.
    # TRANSLIT: kīnahʾī kohanah, dar jang-e Oḥod waqtī peykar pāk-e Ḥamzah Sayyid al-šohadāʾ bar xāk oftādah būd, hamsar-e Abū Sofyān, Hend goft: šekam-e Ḥamzah rā pāreh pāreh kardand wa jegaraš rā bīron āwardand.
    # ENGLISH:  An old grudge — in the Battle of Uhud when the pure body of Hamza had fallen to the ground, Abu Sufyan's wife Hind said: they cut open Hamza's belly and took out his liver.
    # Node 1 کینه‌ای (outer topic/framing device "an old grudge") → nsubj:outer; node 8 پیکر (subject of temporal clause) stays nsubj
    'train-s2108': [('deprel', 1, 'nsubj:outer')],

    # train-s2132
    # TEXT:    هنگامی که زیاد بن امیه از طرف معاویه به عنوان حاکم بصره و کوفه تعیین شد و برای ایراد خطبه بر منبر مسجد جامع کوفه قرار گرفت، و به سوی او سنگ پرتاب شد، زیاد بلافاصله دستور داد درهای مسجد را بستند.
    # TRANSLIT: hangāmī kah Zīyād ebn Amīyyah az ṭaraf Moʿāwīyyah bah ʿonwān ḥākem Baṣrah wa Kūfah taʿyīn šod… Zīyād belāfāṣelah dastūr dād darhāy masjed rā bastand.
    # ENGLISH:  When Ziad ibn Amiya was appointed by Muawiyah as governor of Basra and Kufa… Ziad immediately ordered the mosque doors to be closed.
    # Node 15 تعیین (head of temporal adverbial clause "when he was appointed") → advcl; node 37 زیاد (real subject of main clause) stays nsubj
    'train-s2132': [('deprel', 15, 'advcl')],

    # train-s2148
    # TEXT:    نویسندگان بیانیه با تاسف عمیق از این که دو تفسیر غلط از دوم خرداد وجود دارد، این نعمت ارزشمند را آماج حمله و طعن ساخته است.
    # TRANSLIT: nawīsandagān bayānīyyah bā taʾassof ʿamīq az īn kah do tafsīr ġalaṭ az dovvom-e Xordād wujūd dārad, īn neʿmat arzešmand rā āmāj-e ḥomlah wa ṭaʿn sāxtah ast.
    # ENGLISH:  The writers of the declaration, with deep regret at the fact that two wrong interpretations of the Second of Khordad exist, have made this valuable gift the target of attack and taunt.
    # Node 1 نویسندگان (real agent, outer nsubj re inner clause subject) → nsubj:outer; node 10 تفسیر (subject of embedded existence clause) stays nsubj
    'train-s2148': [('deprel', 1, 'nsubj:outer')],

    # train-s2284
    # TEXT:    پژوهشگران می‌گویند جراحی‌های قلبی که تا کنون با کمک روبات انجام گرفته، همگی نتایج موفقیت‌آمیز داشته‌اند.
    # TRANSLIT: pažūhešgarān mīgūyand jarāḥīhāy qalbī kah tā konūn bā komak-e robāt anjām geraftah, hamgī natāyej movaffaqīyyatāmīz dāštahānd.
    # ENGLISH:  Researchers say that cardiac surgeries that have so far been performed with the help of a robot have all had successful results.
    # Node 3 جراحی‌های (outer topic with relative clause) → nsubj:outer; node 14 همگی (inner subject "all of them") stays nsubj
    'train-s2284': [('deprel', 3, 'nsubj:outer')],

    # train-s2397
    # TEXT:    تحقیقی که توسط دانشگاه کالیفرنیا بر روی موشها انجام شده نشان می‌دهد که اوزون به‌سرعت ویتامین E را که عنصر مهمی برای حفظ سلامت پوست است در لایه فوقانی پوست از بین می‌برد.
    # TRANSLIT: taḥqīqī kah towassoṭ-e Dānešgāh-e Kālīfornīyā bar rūy-e mūšhā anjām šodah nešān mīdahad kah Ōzon bah sorʿat Vītāmīn E rā… az bīn mībarad.
    # ENGLISH:  A study by the University of California on mice shows that ozone rapidly destroys vitamin E in the upper layer of skin.
    # Node 14 اوزون (real subject of می‌برد) stays nsubj; node 16 ویتامین E (direct object marked با را) → obj
    'train-s2397': [('deprel', 16, 'obj')],

    # train-s2468
    # TEXT:    مادر اشک شوق ریخت و پدر از توی صندوق خانه، شیشهٔ بلورینی به دست بچه دیو داد و گفت: هر دیوی یک شیشهٔ عمر دارد.
    # TRANSLIT: mādar ašk-e šowq rīxt wa pedar az tūy-e ṣandūq-e xāna, šīšah-ye bolūrīnī bah dast-e bačča-ye dīw dād wa goft: har dīwī yak šīšah-ye ʿomr dārad.
    # ENGLISH:  The mother shed tears of joy and the father, from inside the chest, gave a crystal vial to the demon-child and said: every demon has a vial of life.
    # Node 1 مادر (real subject) stays nsubj; node 2 اشک (object "tears" in idiom اشک ریخت "shed tears") → obj
    'train-s2468': [('deprel', 2, 'obj')],

    # train-s2539
    # TEXT:    تو هم کتاب قصه داری؟
    # TRANSLIT: to ham ketāb-e qeṣṣah dārī?
    # ENGLISH:  Do you also have a storybook?
    # Node 1 تو (real subject) stays nsubj; node 3 کتاب (object "storybook" of "have") → obj
    'train-s2539': [('deprel', 3, 'obj')],

    # train-s2824
    # TEXT:    سالهای ۱۵ و ۲۵ و ۳۵ یزید از طرف معاویه مسئول حج بود.
    # TRANSLIT: sālhāy 15 wa 25 wa 35 Yazīd az ṭaraf-e Moʿāwīyyah masʾūl-e ḥajj būd.
    # ENGLISH:  In the years 15, 25 and 35, Yazid was in charge of the Hajj on behalf of Muawiyah.
    # Node 1 سالهای (temporal frame "in the years 15, 25 and 35", NOUN head → obl); node 7 یزید (real subject) stays nsubj
    'train-s2824': [('deprel', 1, 'obl')],

    # train-s2871
    # TEXT:    فقط زمانی که طلاق می‌گیرد و جدا می‌شود، شخصیت او معنا پیدا می‌کند…
    # TRANSLIT: faqaṭ zamānī kah ṭalāq mīgerad wa jodā mīšawad, šaxṣīyyat-e ū maʿnā pīdā mīkonad…
    # ENGLISH:  Only when [she] gets a divorce and separates, does her personality find meaning…
    # Node 2 زمانی (temporal clause head "when…", NOUN head → obl); node 10 شخصیت (real subject) stays nsubj
    'train-s2871': [('deprel', 2, 'obl')],

    # train-s3165
    # TEXT:    کاسبرگ خارجی‌ترین بخش است و در داخل آن گلبرگ‌ها و پس از آن پرچم‌ها یا ساختار مذکر تولید مثل و در مرکز نیز مادگی یا ساختار مونت تولید مثل وجود دارد.
    # TRANSLIT: kāsebarg xārejītarīn baxš ast wa dar dāxel-e ān golbargāhā wa pas az ān parčamāhā yā sāxtar-e mozakkar-e towlīd meṯl wa dar markaz nīz mādegī yā sāxtar-e moʾannaṯ-e towlīd meṯl wujūd dārad.
    # ENGLISH:  The sepal is the outermost part and inside it are the petals, and after them the stamens or male reproductive structure, and in the center the pistil or female reproductive structure.
    # Node 9 گلبرگ‌ها (first conjoined subject) stays nsubj; node 24 مادگی (second major conjoined subject) → conj of node 9
    'train-s3165': [('deprel', 24, 'conj')],

    # train-s3288
    # TEXT:    آن کسانی که در جامعه به ارزشها اهمیت می‌دهند، این‌ها مکمل آن کسانی هستند که به تحول و پیشرفت اهمیت می‌دهند.
    # TRANSLIT: ān kasānī kah dar jāmeʿah bah arzešhā ahmīyyat mīdahand, īnhā mokammel-e ān kasānī hastand kah bah taḥawwol wa pīšraft ahmīyyat mīdahand.
    # ENGLISH:  Those who value traditions in society are complementary to those who value change and progress.
    # Node 2 کسانی (outer topic with relative clause) → nsubj:outer; node 11 این‌ها (resumptive pronoun, inner subject) stays nsubj
    'train-s3288': [('deprel', 2, 'nsubj:outer')],

    # train-s3289
    # TEXT:    آن کسانی که به تحول و پیشرفت اهمیت می‌دهند، مکمل آن کسانی بشوند که به ارزشها توجه پیدا می‌کنند.
    # TRANSLIT: ān kasānī kah bah taḥawwol wa pīšraft ahmīyyat mīdahand, mokammel-e ān kasānī bešawand kah bah arzešhā tawajjoh pīdā mīkonand.
    # ENGLISH:  Those who value change and progress should become complementary to those who pay attention to values.
    # Node 2 کسانی (nsubj, the outer topic subject) stays nsubj; node 13 کسانی (genitive/object of مکمل) → reparent to node 11 مکمل, deprel nmod
    'train-s3289': [('reparent', 13, 11, 'nmod')],

    # train-s3321
    # TEXT:    ...این همان چیزی است که بنده چند سال قبل از این، نشانه‌های آن را در گوشه و کنار مشاهده کردم و تهاجم فرهنگی را گفتم...
    # TRANSLIT: …īn hamān čīzī ast kah bandah čand sāl qabl az īn, nešānahāy ān rā dar gūšah wa kenār mošāhedah kardam wa tahājom-e farhangi rā goftam…
    # ENGLISH:  …this is the very thing that I, several years before this, observed signs of here and there and called cultural invasion…
    # Node 36 این (PRON "this") stays nsubj; node 37 همان (DET "the very same") → det of node 38 چیزی
    'train-s3321': [('deprel', 37, 'det')],

    # train-s3330
    # TEXT:    اوایل انقلاب هم یک عده از همینها توانستند امور را قبضه کنند و در دست بگیرند.
    # TRANSLIT: awāyel-e enqelāb ham yak ʿeddah az hamīnhā tawānestand omūr rā qabżah konand wa dar dast begīrand.
    # ENGLISH:  Even in the early days of the revolution a group of these people managed to seize power and take it into their hands.
    # Node 1 اوایل (temporal frame "in the early days of the revolution", NOUN head → obl); node 5 عده (real subject) stays nsubj
    'train-s3330': [('deprel', 1, 'obl')],

    # train-s3372
    # TEXT:    مگر نه این بود شعار براندازی حکومت شاه، شعار بسیاری از سازمانهای چریکی و مبارزان مسلح مارکسیست و غیرمارکسیست بود و مگر نه این که حتی نیروهای ملی مذهبی و ملی‌گرایان هم در هفته‌ها و روزهای نزدیک به پیروزی انقلاب، دیگر شعار شاه باید سلطنت کند، نه حکومت را تکرار نمی‌کردند...
    # TRANSLIT: magar nah īn būd šeʿār-e barāndāzī-e ḥokūmat-e Šāh, šeʿār-e besyārī az sāzmānhāy čerīkī…magar nah īn kah ḥattā nīrūhāy mellī-ye mazhabi wa mellīgarāyān ham…dīgar šeʿār-e «Šāh bāyad salṭanat konad, nah ḥokūmat» rā takrār namīkardand…
    # ENGLISH:  Was it not the case that the slogan of overthrowing the Shah's rule was the slogan of many guerrilla organizations… and wasn't it the case that even national-religious forces were no longer repeating the slogan "The Shah should reign, not rule"…
    # Node 28 نیروهای (real subject of نمی‌کردند) stays nsubj; node 44 شعار (object "the slogan" which was not repeated, marked by را) → obj
    'train-s3372': [('deprel', 44, 'obj')],

    # train-s3828
    # TEXT:    آن خبرنگار که داستان لواسان او را هراسان کرده، دلیلش چه بوده؟
    # TRANSLIT: ān xabarnagār kah dāstān-e Lavāsān ū rā harāsān kardah, dalīllaš čah bodah?
    # ENGLISH:  That reporter who was frightened by the Lavasan story — what has been the reason?
    # Node 2 خبرنگار (outer topic "that reporter who…") → nsubj:outer; node 11 دلیل (inner subject "the reason") stays nsubj
    'train-s3828': [('deprel', 2, 'nsubj:outer')],

    # train-s3895
    # TEXT:    این اخترشناسان گفتند که آلبرت ۹۱۷ که از فاصله ۶ / ۳۰ میلیون کیلومتری زمین می‌گذرد، هیچ خطری برای زمین ایجاد نمی‌کند.
    # TRANSLIT: īn axteršenāsān goftand kah Ālbert 917 kah az fāṣelah-ye 30.6 mīlīyon kīlometri-ye zamīn mīgozarad, hīč xaṭarī barāy zamīn ījād namīkonad.
    # ENGLISH:  These astronomers said that asteroid Albert 917, which passes at a distance of 30.6 million kilometers from Earth, poses no danger to Earth.
    # Node 5 آلبرت (outer topic with relative clause "which passes at…") → nsubj:outer; node 19 خطری (inner subject "any danger") stays nsubj
    'train-s3895': [('deprel', 5, 'nsubj:outer')],

    # train-s3925
    # TEXT:    ای سرزمین آسمانی فردوسی، آیا این روس خیال‌پرداز را که دیدگانی ساده و پر‌رویا داشت و مدتی مهمان تو بود، فراموش خواهی کرد؟
    # TRANSLIT: ay sarzamīn-e āsmānī-ye Ferdowsī, āyā īn Ros-e xeyālpardāz rā kah dīdegānī sādah wa por-royā dāšt wa moddatī mehmmān-e to būd, farāmuš xāhī kard?
    # ENGLISH:  O heavenly land of Ferdowsi, will you forget this imaginative Russian who had simple and dreamy eyes and was your guest for a time?
    # Node 2 سرزمین (vocative address "O heavenly land") → vocative; node 8 روس (direct object with را) → obj
    'train-s3925': [('deprel', 2, 'vocative'), ('deprel', 8, 'obj')],

    # train-s3981
    # TEXT:    باری این روزها، ما که در هتل صفاییه یزد جای گزیده بودیم، من هرروز صبح که برای ناشتائی در سالن چشم‌انداز، چشم به کاج‌های بلند باغ می‌انداختم، در همان لحظه یکی از دوستان وارد می‌شد و می‌گفت: آقای باستانی، روزنامه اطلاعات دیروز را دیدی؟
    # TRANSLIT: bārī īn rūzhā, mā kah dar hotel-e Ṣafāʾīyyah-ye Yazd jā gozīdah bōdīm, man hārrūz ṣobḥ kah barāy nāšetāʾī dar sālon-e češmandāz, češm bah kājhāy-e boland-e bāġ mīandāxtam, dar hamān laḥẓah yakī az dustān wāred mīšod wa mīgoft: āqāy Bāstānī, rūznāmah-ye Eṭṭelāʿāt-e dīrūz rā dīdī?
    # ENGLISH:  Well, in those days, we who were staying at the Safaiyeh hotel in Yazd, I every morning when I cast my eyes on the tall pines of the garden, at that very moment one of my friends would come in and say: Mr. Bastani, did you see yesterday's Ettela'at?
    # Node 15 من (subject of advcl clause می‌انداختم) → nsubj:outer; node 35 یکی (real subject of main clause وارد می‌شد) stays nsubj
    'train-s3981': [('deprel', 15, 'nsubj:outer')],

    # train-s4314
    # TEXT:    وی اهم فعالیت خود را نظارت بر مطبوعات و سایر فعالیت‌های فرهنگی قرار داده است.
    # TRANSLIT: wī ahamm faʿālīyyat-e xod rā neẓārat bar maṭbūʿāt wa sāyer faʿālīyyathāy farhangī qarār dādah ast.
    # ENGLISH:  He/She has designated their primary activity as oversight of the press and other cultural activities.
    # Node 1 وی (real subject) stays nsubj; node 6 نظارت (predicate complement of قرار داده) → xcomp
    'train-s4314': [('deprel', 6, 'xcomp')],

    # train-s4500
    # TEXT:    دکتر گود، مسئول مطالعه از دانشگاه کلمبیا، در همایش پیشگیری از خودکشی به رواج پدیده خودکشی به‌خصوص در بین نوجوانان اشاره کرد و افزود: رسانه‌ها نقش مهمی در انتقال انگیزه خودکشی به افراد مستعد دارند.
    # TRANSLIT: Doktor Gūd, masʾūl-e moṭāleʿah az Dānešgāh-e Kolombīyā, dar hamāyeš-e pīšgīrī az xodkoši bah rawāj-e padīdah-ye xodkoši baxuṣūṣ dar beyn-e nowjavānān ešārah kard wa afzūd: resānehā naqš-e mohhemmī dar entqāl-e angīzah-ye xodkoši bah afrād-e mostaʿedd dārand.
    # ENGLISH:  Dr. Good, the study director from Columbia University, referred to the spread of the suicide phenomenon and added: Media have an important role in transmitting the motivation for suicide to susceptible individuals.
    # Node 28 رسانه‌ها (real subject "media") stays nsubj; node 29 نقش (object "role" of "have") → obj
    'train-s4500': [('deprel', 29, 'obj')],

    # train-s4620
    # TEXT:    از مطالعهٔ تذکرهٔ شام غریبان و دیگر تذکره‌ها معلوم می‌گردد که در کاروان هند بعضی از شعرای وارد‌شده به هند ذکر نشده‌اند و از جمله کسانی که در عصر گورکانیان از آسیای مرکزی آمدند می‌توان افرادی همچون قاسم کاهی، مولانا حسین مروی و غیره را نام برد که شهرت فراوان دارند...
    # TRANSLIT: az moṭāleʿah-ye Tazkerah-ye Šām Gharībān wa dīgar tazkerehā maʿlūm mīgardad kah dar kārawān-e Hend baʿḍī az šoʿarāy wāredšodah bah Hend zekr našodahānd wa az jomlah kasānī kah dar ʿaṣr-e Gurkānīyān az Āsyāy-e Markazī āmadand mītawān afrādī hamčon Qāsem Kāhī… nām bord…
    # ENGLISH:  From studying the Sham-e Ghariban tazkirah, it becomes clear that some of the poets who entered India are not mentioned, and among those who came from Central Asia in the Gurkani era one can name individuals such as Qasim Kahi…
    # Node 15 بعضی (outer topic, first conjoined subject of first clause) → nsubj:outer; node 26 کسانی (subject of second coordinated clause) stays nsubj
    'train-s4620': [('deprel', 15, 'nsubj:outer')],

    # train-s4687
    # TEXT:    خلاصه این که موضوع فیضی تربتی روشن نیست و سخن نفایس و غیره در چشم‌پوشی از او انکار ورود وی به هند و ارتباطش با دربار اکبر درست نیست.
    # TRANSLIT: xolāṣah īn kah mowżūʿ-e Fayżī Torbatī rowšan nīst wa soxan-e Nafāyes wa ġayrah dar češmpūšī az ū enkār-e worūd-e wī bah Hend wa ertebāṭaš bā darbār-e Akbar dorost nīst.
    # ENGLISH:  In summary, the matter of Faizi Torbati is not clear, and the speech of Nafayis and others regarding ignoring him — denying his entry to India and his relationship with the court of Akbar — is not correct.
    # Node 10 سخن (first conjoined subject "the speech") stays nsubj; node 18 انکار (second conjoined subject "the denial") → conj of node 10
    'train-s4687': [('deprel', 18, 'conj')],

    # ══════════════════════════════════════════════════════════════════════
    # DEV SPLIT
    # ══════════════════════════════════════════════════════════════════════

    # dev-s118
    # TEXT:    معاویه می‌پنداشت او اگر نام حسین) ع (را نبرد و حسین) ع (را سرور و بزرگ بنی‌هاشم نداند امور واقع چنان که او می‌خواهد شکل می‌گیرد.
    # TRANSLIT: Moʿāwīyyah mīpandāšt ū agar nām-e Ḥosayn (ʿ) rā nabarad wa Ḥosayn (ʿ) rā sarwar wa bozorg-e Banīhāšem nadānad omūr-e wāqeʿ čonān kah ū mīxāhad šekl mīgīrad.
    # ENGLISH:  Muawiyah thought that if he didn't mention Husayn's name and didn't acknowledge Husayn as lord of Bani Hashim, actual matters would take shape as he wished.
    # Node 23 امور (subject of می‌گیرد) → reparent to node 30 می‌گیرد, deprel nsubj; node 27 او (subject of می‌خواهد) stays nsubj there
    'dev-s118': [('reparent', 23, 30, 'nsubj')],

    # dev-s280
    # TEXT:    بسیاری از صاحبنظران و منتقدان، برای فیلم تخته‌سیاه که با استقبال فراوانی روبه‌رو شده، جایزه نخل طلا و گروهی دیگر، دست‌کم یکی از جوایز بخش مسابقه را پیش‌بینی می‌کنند.
    # TRANSLIT: besyārī az ṣāḥibnażarān wa montaqedān, barāy film-e Taxteye-Sīyāh kah bā estiqbāl-e farāwānī rūbahrū šodah, jāyezah-ye Naxl-e Ṭalā wa gorūhī dīgar, dast-kam yakī az jawāyez-e baxš-e mosābaqah rā pīšbīnī mīkonand.
    # ENGLISH:  Many critics and analysts predict the Palme d'Or for the film Blackboard, and another group predict at least one of the competition prizes.
    # Node 1 بسیاری (first conjoined subject) stays nsubj; node 21 گروهی (second conjoined subject "another group") → conj of node 1
    'dev-s280': [('deprel', 21, 'conj')],

    # dev-s296
    # TEXT:    تکرار مقام چهارمی، بازهم با ۳ مدال تیم ایران به مقام چهارمی چهاردهمین دوره مسابقه‌های تکواندو قهرمانی آسیا - اقیانوسیه که در هنگ‌کنگ چین جریان داشت، دست یافت.
    # TRANSLIT: tekrār-e maqām-e čahāromī, bāzham bā 3 medāl tīm-e Īrān bah maqām-e čahāromī-ye čahārdahomīn dawrah-ye mosābaqahāy-e takkwāndū-ye qahramānī-ye Āsyā-Oqyānūsīyyah kah dar Hong Kong-e Čīn jareyān dāšt, dast yāft.
    # ENGLISH:  Repeating 4th place — again with 3 medals the Iranian team achieved 4th place in the 14th Asia-Oceania Taekwondo Championships held in Hong Kong, China.
    # Node 1 تکرار (outer topic, headline-style summary phrase) → nsubj:outer; node 9 تیم (real subject) stays nsubj
    'dev-s296': [('deprel', 1, 'nsubj:outer')],

    # dev-s305
    # TEXT:    بهمن طهماسبی در دقیقه ۲ برای تیم استقلال تهران و امیدرضا رمضانی در دقیقه ۷۱ برای تیم ایرسوتر در این دیدار گلزنی کردند.
    # TRANSLIT: Bahman Ṭahmāsebī dar daqīqah-ye 2 barāy tīm-e Esteqlāl-e Tehrān wa Omīdreżā Ramaẓānī dar daqīqah-ye 71 barāy tīm-e Eyrsūter dar īn dīdār golzanī kardand.
    # ENGLISH:  Bahman Tahmasbi in minute 2 for Esteghlal Tehran and Omidreza Ramzani in minute 71 for Airsoter scored goals in this match.
    # Node 1 بهمن (first conjoined subject) stays nsubj; node 11 امیدرضا (second conjoined subject) → conj of node 1
    'dev-s305': [('deprel', 11, 'conj')],

    # dev-s479
    # TEXT:    وصله الحاقی، هر گونه فایل ضمیمه‌ای میل را که کد ویژوال‌بیسیک داشته باشد، مسدود می‌کند.
    # TRANSLIT: waṣlah-ye elḥāqī, har gonah fāyl-e żamīmahʾī meyl rā kah kod-e Vīžuāl Beysek dāšta bāšad, masdūd mīkonad.
    # ENGLISH:  The add-on patch blocks any email attachment file that has Visual Basic code.
    # Node 1 وصله (real subject) stays nsubj; node 6 فایل (direct object marked with را) → obj
    'dev-s479': [('deprel', 6, 'obj')],

    # ══════════════════════════════════════════════════════════════════════
    # TEST SPLIT
    # ══════════════════════════════════════════════════════════════════════

    # test-s16
    # TEXT:    هوا پرخروش و زمین پر ز جوش، خنک آن که دل شاد دارد به نوش.
    # TRANSLIT: hawā por-xorūš wa zamīn por ze jūš, xonak ān kah del-e šād dārad bah nūš.
    # ENGLISH:  The air is stormy and the earth is full of turmoil, lucky is one who keeps a merry heart at drinking.
    # Node 1 هوا (subject of first conjunct) stays nsubj; node 4 زمین (subject of second conjunct, parallel) → reparent to node 1, deprel conj
    'test-s16': [('reparent', 4, 1, 'conj')],

    # test-s188
    # TEXT:    وی روابط بازرگانی هند و ایران را در حال گسترش توصیف کرد و افزود: در سال ۱۹۹۹ صادرات هند به ایران به ۷۵۱ میلیون دلار و واردات از ایران به ۱۸۴ میلیون دلار بالغ شد.
    # TRANSLIT: wī rawābeṭ-e bāzargānī-ye Hend wa Īrān rā dar ḥāl-e gostareš towṣīf kard wa afzūd: dar sāl-e 1999 ṣāderāt-e Hend bah Īrān bah 751 mīlīyon dolār wa wāredāt az Īrān bah 184 mīlīyon dolār bāleġ šod.
    # ENGLISH:  He described India-Iran trade relations as expanding and added: in 1999 India's exports to Iran amounted to 751 million dollars and imports from Iran to 184 million dollars.
    # Node 19 صادرات (first conjoined subject) stays nsubj; node 28 واردات (second conjoined subject) → conj of node 19
    'test-s188': [('deprel', 28, 'conj')],

    # test-s189
    # TEXT:    وی افزود: ارزش واردات نفتی هند از ایران در سال ۹۹ میلادی ۲۵۰ میلیون دلار و واردات غیرنفتی از ایران ۷۲۲ میلیون دلار برآورد شده است.
    # TRANSLIT: wī afzūd: arzaš-e wāredāt-e naftī-ye Hend az Īrān dar sāl-e 99-e mīlādī 250 mīlīyon dolār wa wāredāt-e ġayrnaftī az Īrān 722 mīlīyon dolār barāward šodah ast.
    # ENGLISH:  He added: the value of India's oil imports from Iran in year 99 was estimated at 250 million dollars and non-oil imports from Iran 722 million dollars.
    # Node 4 ارزش (first conjoined subject) stays nsubj; node 18 واردات (second conjoined subject) → conj of node 4
    'test-s189': [('deprel', 18, 'conj')],

    # test-s411
    # TEXT:    این مرکز که دارای ۲ هزار و ۷۴۰ متر زیربناست در زمینی به مساحت ۱۸ هزار و ۴۶ متر، اهدایی اهالی روستای خوزنین احداث شده است.
    # TRANSLIT: īn markaz kah dārāy 2 hezār wa 740 metr-e zīrbanāst dar zamīnī bah masāḥat-e 18 hezār wa 46 metr, ehdāyī-ye ahālī-ye rowstāy-e Xooznīn eḥdāṯ šodah ast.
    # ENGLISH:  This center, which has 2740 square meters of floor space, in a land of 18046 square meters, donated by the residents of Khoznin village, has been constructed.
    # Node 2 مرکز (real subject) stays nsubj:pass; node 22 اهدایی (appositive modifier "donated by the residents") → appos of node 2
    'test-s411': [('deprel', 22, 'appos')],

    # test-s466
    # TEXT:    در یک طرف این سنگ‌نگاره نقش سه سرباز جاویدان با سپر و نیزه و در طرف دیگر آن نقش دو سرباز پارسی با نیزه حک شده است.
    # TRANSLIT: dar yak ṭaraf-e īn sangnegārah naqš-e seh sarbāz-e jāwīdān bā separ wa neyza wa dar ṭaraf-e dīgar-e ān naqš-e do sarbāz-e Pārsī bā neyza ḥakk šodah ast.
    # ENGLISH:  On one side of this relief is the design of three Immortal soldiers with shield and spear and on the other side the design of two Persian soldiers with a spear has been carved.
    # Node 6 نقش (first conjoined subject) stays nsubj; node 19 نقش (second conjoined subject) → conj of node 6
    'test-s466': [('deprel', 19, 'conj')],

    # test-s565
    # TEXT:    تیم ذوب‌آهن اصفهان نمایندهٔ ایران در این مسابقه‌ها آخرین بازی خود را مقابل تیم الوحده سوریه انجام خواهد داد.
    # TRANSLIT: tīm-e Zob-Āhan-e Eṣfahān namāyandeye Īrān dar īn mosābaqahā āxerīn bāzī-ye xod rā moqābel-e tīm-e Al-Waḥdah-ye Surīyyah anjām xāhad dād.
    # ENGLISH:  The Zob Ahan Isfahan team, Iran's representative in these competitions, will play their last match against Al-Wahda Syria team.
    # Node 1 تیم (real subject) stays nsubj; node 4 نمایندهٔ (appositive "Iran's representative") → appos of node 1
    'test-s565': [('deprel', 4, 'appos')],

    # test-s595
    # TEXT:    استاد جلال‌الدین همایی نیز کتاب شرح‌ما‌اشکل را که تا زمان او به صورتهای نامنقح به چاپ رسیده بود، تصحیح و به فارسی ترجمه و جزء کتاب خیامی‌نامه خود منتشر کرد ۶.
    # TRANSLIT: Ostād Jalāloddīn Homāyī nīz ketāb-e Šarḥ-mā-aškala rā kah tā zamān-e ū bah ṣūrathāy-e nāmonqaḥ bah čāp resīdah būd, taṣḥīḥ wa bah Fārsī tarjomah wa jozʾ-e ketāb-e Xayyāmīnāmah-ye xod montašer kard 6.
    # ENGLISH:  Professor Jalal al-Din Homaei also corrected the book Sharh-ma-ashkal, translated it into Persian, and published it as part of his Khayyami-nameh.
    # Node 1 استاد (real subject) stays nsubj; node 5 کتاب (direct object marked with را) → obj
    'test-s595': [('deprel', 5, 'obj')],
}


def apply_fixes(doc, fixes):
    fixed = 0
    for bundle in doc.bundles:
        for tree in bundle.trees:
            sid = tree.sent_id
            if sid not in fixes:
                continue
            nodes = {n.ord: n for n in tree.descendants}
            for op in fixes[sid]:
                if op[0] == 'deprel':
                    _, nid, new_deprel = op
                    nodes[nid].deprel = new_deprel
                elif op[0] == 'reparent':
                    _, nid, new_head_id, new_deprel = op
                    nodes[nid].parent = nodes[new_head_id]
                    nodes[nid].deprel = new_deprel
            fixed += 1
    return fixed


if __name__ == '__main__':
    base = os.path.expanduser('.')
    splits = {
        'train': os.path.join(base, 'fa_seraji-ud-train.conllu'),
        'dev':   os.path.join(base, 'fa_seraji-ud-dev.conllu'),
        'test':  os.path.join(base, 'fa_seraji-ud-test.conllu'),
    }
    for split, path in splits.items():
        doc = udapi.Document(path)
        n = apply_fixes(doc, FIXES)
        doc.store_conllu(path)
        print(f"Fixed {n} sentences in {path}")
