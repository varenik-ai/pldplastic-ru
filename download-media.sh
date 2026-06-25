#!/bin/bash
# ================================================================
# SUPULIDE — скрипт скачивания всех медиафайлов с CDN
# Запустить из папки pldplastic-ru:
#   bash download-media.sh
# ================================================================

set -e
BASE="https://omo-oss-image.thefastimg.com/portal-saas/pg2024042811332048086/cms/image"
VIDEO_BASE="https://omo-oss-video110.thefastvideo.com/portal-saas/pg2024042811332048086/cms/vedio"

mkdir -p img

REFERER="http://www.pldplastic.com/"

echo "📥 Скачивание изображений с CDN оригинального сайта..."
echo ""

download() {
  local url="$1"
  local file="$2"
  if [ -f "img/$file" ]; then
    echo "  ✓ (уже есть) img/$file"
  else
    echo "  ↓ $file"
    curl -s -L --referer "$REFERER" \
         -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36" \
         -o "img/$file" "$url"
    if [ $? -eq 0 ] && [ -s "img/$file" ]; then
      echo "    ✅ OK ($(du -h img/$file | cut -f1))"
    else
      echo "    ❌ Ошибка — файл не скачан или пустой"
      rm -f "img/$file"
    fi
  fi
}

# Логотипы
download "$BASE/a86d1385-27fb-46b0-8bf7-8e2788fff8a7.png"  "logo.png"
download "$BASE/37b247a2-09b4-49d1-97dc-f5297bc58db6.png"  "logo-footer.png"
download "$BASE/94a41dbd-0835-4ef5-998f-a4ade8928362.png"  "logo-footer2.png"

# Слайдер
download "$BASE/74b9c9d4-685b-4ed7-a69f-922b4d6a01b6.jpg"  "hero-1.jpg"
download "$BASE/6a3cc060-da56-4211-9afe-aa17e82ddd98.jpg"   "hero-2.jpg"

# Видео
download "$BASE/7fbf926f-c482-43ca-b738-14cd69dc15ba.jpg"   "video-thumb.jpg"

# Карусель приложений (应用领域) — 7 позиций из API
download "$BASE/8cff4b3c-70c5-45c6-816f-8b924f417c33.jpg"   "app-eaa.jpg"
download "$BASE/f9bf2b41-cd20-4d93-b23a-8f9c28258a25.jpg"   "app-emaa.jpg"
download "$BASE/003dc0f4-d31d-4d64-b81d-2e10cb687bef.jpg"   "app-eva.jpg"
download "$BASE/b1e50621-8b3d-4f76-8b67-8ed4222f75fb.jpg"   "app-poe.jpg"
download "$BASE/ae8da5fa-98bf-4916-87d3-f99299d8539e.jpg"   "app-evoh.jpg"
download "$BASE/36d9a7e0-8f9c-4226-b2fb-62b2fffcb414.jpg"   "app-pmaa.jpg"
download "$BASE/87741e9c-7ef5-4aad-b069-01417f09faa4.jpg"   "app-abspec.jpg"

# Преимущества
download "$BASE/e42b3e63-a842-44ad-8b6f-6fdba6852dcd.jpg"   "adv-tech.jpg"
download "$BASE/0d7bb535-5c37-4d6a-9df5-857dd8f4ced5.jpg"   "adv-team.jpg"
download "$BASE/d789b723-8fb9-4739-be1e-eee5dd4dd8d2.jpg"   "adv-resources.jpg"

# Новости
download "$BASE/2b9a84ba-167c-4af1-8057-94d376c13142.jpeg"  "news-main.jpeg"

# Карта мира
download "$BASE/79ae380f-1538-4866-9fe1-aa5fe0836d54.png"   "world-map.png"

# ── СТРАНИЦА НОВОСТЕЙ (news.html) ────────────────────────────────
# Герой-баннер новостей
download "$BASE/93915cc5-7fc4-4878-9d0d-5604be151966.webp" "news-hero.webp"

# Статья 1: «Взаимосвязь пигментов, пластикового сырья и вспомогательных веществ»
download "$BASE/63109afe-fb09-46b5-8e7f-22e3e32cd48e.jpg"  "news-1.jpg"
# Статья 2 и 4 (одна картинка): «PBT» / «Утечки гидросистемы»
download "$BASE/a59503f0-7d4c-4d43-a41e-0eeb499da51d.jpg"  "news-2.jpg"
# Статья 3: «Параметры литья под давлением»
download "$BASE/d0425e72-7a31-45d5-944f-0a735f603ff9.jpg"  "news-3.jpg"

# ── СТРАНИЦА НОВОСТЕЙ ОТРАСЛИ (news-industry.html) ────────────────
# Статья 2: «Высокоэффективные пластики — физико-химические свойства»
download "$BASE/73ac14fa-1553-44d7-a051-7981c6d2be18.jpeg" "ind-1.jpeg"
# Статья 3 и 5: «Модифицированные пластики» / «Автомобильный рынок»
download "$BASE/bbd2c5e4-9bdd-42c9-a4cf-91a33712e6ab.jpg"  "ind-2.jpg"

# ── СТРАНИЦА О КОМПАНИИ (about.html) ──────────────────────────────
# Герой-баннер
download "$BASE/c9377bb0-6016-4652-b955-2606c6b23794.jpg"   "about-hero.jpg"
# Превью видео
download "$BASE/3b507ffd-c3c1-4cf2-81a7-ef22022e9f2e.jpg"   "about-video.jpg"

# ── СТРАНИЦА ПРОДУКТОВ (products.html + product-XXX.html) ─────────
# Герой-баннер
download "$BASE/b24b9e9b-4566-4433-bd01-9dc4a33d2f55.jpg"   "prod-hero.jpg"

# Иконки применения — страница POE (и других продуктов)
download "$BASE/693d4231-9fe5-4ef8-9d8a-ffce80ec61c5.png"   "icon-auto.png"
download "$BASE/e4ec2c8e-e84b-4d7b-9aa5-f017681c7415.png"   "icon-cable.png"
download "$BASE/a57f11cf-e291-4558-947c-a5ddc98617a6.png"   "icon-solar.png"
download "$BASE/53fc6f4d-7604-4477-92ed-f7eab3e28045.png"   "icon-film.png"
download "$BASE/cf18b3bc-3fdf-4c36-a3b0-1d691e37b06b.png"   "icon-appliance.png"
download "$BASE/c4342da3-ffbb-4896-a793-cc93e8e79029.png"   "icon-shoe.png"

# Иконки применения — страница POP
download "$BASE/d80a1d9c-729f-4fd9-a9ed-51c95ff8f8eb.png"   "icon-pop-veg.png"
download "$BASE/57d8e2d1-17c1-4474-b6d3-818d8a88cbdb.png"   "icon-pop-meat.png"
download "$BASE/128cf720-67a7-4abc-9553-49494e20819b.png"   "icon-pop-milk.png"
download "$BASE/2650ab02-edb1-41e0-93dd-e0e3c1a585dc.png"   "icon-pop-medical.png"
download "$BASE/68de0189-f486-4c85-8314-d36a3259ca85.png"   "icon-pop-diaper.png"
download "$BASE/aa86ce13-b3d5-403d-8ee3-dfa4dd6bf098.png"   "icon-pop-detergent.png"
# Иконки применения — страница EPDM
download "$BASE/f112e2ca-4a1b-4288-985d-ca42bd3c67d7.jpg"   "icon-epdm-cable.jpg"
download "$BASE/106403ce-c77f-474d-8845-ee6a3920ce21.jpg"   "icon-epdm-pipe.jpg"
download "$BASE/77192444-94c6-4428-845d-33e3e815f72c.jpg"   "icon-epdm-shoe.jpg"
# icon-epdm-profile.jpg, icon-epdm-seal.jpg, icon-epdm-auto.jpg — нет UUID, используют fallback adv-tech.jpg

# Иконки применения — страница MLLDPE (все 6 с UUID)
download "$BASE/6990a9e1-d568-468d-a3aa-56c23c401d2f.png"   "icon-mlldpe-water.png"
download "$BASE/155e404c-0bd8-45d2-80d2-c32054507737.png"   "icon-mlldpe-drink.png"
download "$BASE/af633c90-5c57-4a3d-b8ed-f609650449ed.png"   "icon-mlldpe-pallet.png"
download "$BASE/164ab8b1-60c3-419b-8442-56eb247ce46e.png"   "icon-mlldpe-stretch.png"
download "$BASE/f02838fa-b675-42d3-bb09-0d16b8e50050.png"   "icon-mlldpe-bag.png"
download "$BASE/d6747676-92b9-4b11-a6e3-bbfce09bca14.png"   "icon-mlldpe-flex.png"

# Изображение продукта и иконки применения — страница XLPE
download "$BASE/8f8c7958-f6ed-436c-aeaf-2b29431507b0.jpg"   "prod-xlpe.jpg"
download "$BASE/23568172-ad17-45fd-8810-4b03b9a421b8.jpg"   "icon-xlpe-auto.jpg"
download "$BASE/168a11a8-46d1-485f-ab9f-d476d8489ca1.jpg"   "icon-xlpe-hv.jpg"
download "$BASE/3ebf4e95-03fe-4ea5-98b6-db6a9788e16a.jpg"   "icon-xlpe-wire.jpg"

# Изображение продукта и иконки применения — страница PC
download "$BASE/8e7b1afa-7a05-4ac6-a71f-638bc77a66e4.jpg"   "prod-pc.jpg"
download "$BASE/c14bdd80-b8a8-4784-8498-18a4f44bc508.jpg"   "icon-pc-auto.jpg"
download "$BASE/2a153fe1-7ee5-4616-9c13-323c11abccdc.jpg"   "icon-pc-switch.jpg"
download "$BASE/40786dd4-131d-4bc5-8fc0-37008247462b.jpg"   "icon-pc-bottle.jpg"
download "$BASE/75b43734-40ce-488f-b7e9-76598327adbb.jpg"   "icon-pc-computer.jpg"
download "$BASE/bd4ad60a-38fa-4935-b0dc-d18c9598eca0.jpg"   "icon-pc-sheet.jpg"
download "$BASE/c5f73de0-26d6-4dc9-882f-c7e128abe13d.jpg"   "icon-pc-optics.jpg"

# Изображение продукта и иконки применения — страница PC/ABS
download "$BASE/f67821aa-1eae-49b7-999f-2f284cdbb615.jpg"   "prod-pcabs.jpg"
download "$BASE/7a788fd2-0a7d-46d8-8ef6-427204c89c14.jpg"   "icon-pcabs-auto.jpg"
download "$BASE/ca2a4733-2fd7-4228-8a2d-32c66ffd1e23.jpg"   "icon-pcabs-equipment.jpg"
download "$BASE/1edc59a1-1630-4fa3-81c3-a78c1c53df7c.jpg"   "icon-pcabs-phone.jpg"
download "$BASE/4788570a-59c2-4946-8ec9-e9835a8a56c4.jpg"   "icon-pcabs-electric.jpg"
download "$BASE/4d0e991f-88b5-4aa7-a157-2630c768a4fb.jpg"   "icon-pcabs-appliance.jpg"
download "$BASE/9759ea9b-746b-4bb9-ae82-a77283038bfa.jpg"   "icon-pcabs-computer.jpg"

# Изображение продукта и иконки применения — страница PMMA
download "$BASE/8f8c7958-f6ed-436c-aeaf-2b29431507b0.jpg"   "prod-pmma.jpg"
download "$BASE/2b193c87-5265-4590-8775-5a11c2dfe953.jpg"   "icon-pmma-lamp.jpg"
download "$BASE/d3133655-4f26-43ad-945c-e7b1ee3d5735.jpg"   "icon-pmma-lens.jpg"
download "$BASE/38fe8236-e1be-43eb-a62a-a91a0aa2ebe3.jpg"   "icon-pmma-dash.jpg"

# Изображение продукта и иконки применения — страница POM
download "$BASE/26bbbeb8-471f-4877-b048-025dc5d3f97a.jpg"   "prod-pom.jpg"
download "$BASE/58659957-5200-4849-9c3d-e34241304dbd.jpg"   "icon-pom-gear.jpg"
download "$BASE/54337328-c8be-4b96-868a-2f2e1e5a93bd.jpg"   "icon-pom-music.jpg"
download "$BASE/88fc1293-fa71-4ead-a85c-a0d435899ff4.jpg"   "icon-pom-auto.jpg"

# Изображение продукта и иконки применения — страница PA66
download "$BASE/accf6f68-2032-413d-8e4f-7c45531bafea.jpg"   "prod-pa66.jpg"
download "$BASE/980d0488-bd6e-491b-9ba9-323f727cd368.jpg"   "icon-pa66-edge.jpg"
download "$BASE/a4386ade-b6d6-4333-845c-6c7e42a9ff1d.jpg"   "icon-pa66-power.jpg"
download "$BASE/063f2df1-5d1e-49c9-8b19-25be96c81834.jpg"   "icon-pa66-charger.jpg"
download "$BASE/d7d5d598-5f30-4dd9-ad35-103535fd3619.jpg"   "icon-pa66-gear.jpg"
download "$BASE/a63b6ea0-537a-4d65-bc25-409f5534c5fa.jpg"   "icon-pa66-pipe.jpg"
download "$BASE/a1bc381e-aea2-4e23-9760-9a454b2edda7.jpg"   "icon-pa66-auto.jpg"

# Изображение продукта и иконки применения — страница LCP
download "$BASE/98767a85-e0f7-458e-8260-18be658f63ef.jpg"   "prod-lcp.jpg"
download "$BASE/12317dfe-5710-4fd2-a544-8b798cbb3c7f.jpg"   "icon-lcp-usb.jpg"
download "$BASE/145b2188-9a5c-4836-b205-a5748a7ea3d2.jpg"   "icon-lcp-switch.jpg"
download "$BASE/082567ff-b591-4449-aca5-bfbbff9655c6.jpg"   "icon-lcp-reflector.jpg"
download "$BASE/050bbb3b-2c91-45f1-9ed3-da0b100d6e31.jpg"   "icon-lcp-dental.jpg"

# Изображение продукта и иконки применения — страница PPSU
download "$BASE/4cd71dff-4730-4311-b127-78da665d025c.jpg"   "prod-ppsu.jpg"
download "$BASE/e207e7cd-635b-48ff-a485-b900438e8f51.jpg"   "icon-ppsu-insulator.jpg"
download "$BASE/8932f98b-44bb-405b-8bff-a7c57f4e2c89.jpg"   "icon-ppsu-instrument.jpg"
download "$BASE/39593e32-fe81-47e6-8af8-8cf5e2c30940.jpg"   "icon-ppsu-circuit.jpg"
download "$BASE/ec64c91d-4afa-4c45-b166-c86de7cd5900.jpg"   "icon-ppsu-appliance.jpg"
download "$BASE/9110b858-3234-415c-b713-fb27b961fcff.jpg"   "icon-ppsu-gasmask.jpg"
download "$BASE/3e59a729-f3d4-42b3-b6d1-12937065cb1c.jpg"   "icon-ppsu-bottle.jpg"

# Изображение продукта и иконки применения — страница PSU
download "$BASE/3ba6fdfa-adb6-422e-b0d6-bca6d0609ec2.jpg"   "prod-psu.jpg"
download "$BASE/4a5c2aa2-d285-472c-8d2d-8a959638f96b.jpg"   "icon-psu-connector.jpg"
download "$BASE/9d4c7e44-edf5-4efd-a6b1-d73ce22618d3.jpg"   "icon-psu-sensor.jpg"

# Изображение продукта и иконки применения — страница PES
download "$BASE/accf6f68-2032-413d-8e4f-7c45531bafea.jpg"   "prod-pes.jpg"
download "$BASE/f0a358ee-e6c3-4a51-89b9-705f8a61fa9f.jpg"   "icon-pes-ev.jpg"
download "$BASE/2023ac50-79a7-48ca-9c3e-c9b8a566592f.jpg"   "icon-pes-filter.jpg"
download "$BASE/b6aa1c07-e81b-4417-8c92-1efc0e8127fa.jpg"   "icon-pes-coil.jpg"
download "$BASE/f55834a7-7c78-4486-9de2-f9b7108c6c17.jpg"   "icon-pes-aircraft.jpg"

# Изображение продукта и иконки применения — страница PA12
download "$BASE/8e7b1afa-7a05-4ac6-a71f-638bc77a66e4.jpg"   "prod-pa12.jpg"
download "$BASE/6e3ef03b-8a35-49db-bdc2-1bc57ca3b6a3.jpg"   "icon-pa12-auto.jpg"
download "$BASE/7e023b15-1418-4b0a-9bbd-20fcc65f976d.jpg"   "icon-pa12-cable.jpg"
download "$BASE/a9b14cdd-82ea-455f-b9ee-1dd0583bba9b.jpg"   "icon-pa12-3d.jpg"
download "$BASE/ec83bed1-bbf8-4e72-bba4-2b7f3da1576a.jpg"   "icon-pa12-powder.jpg"
download "$BASE/ca83a6ad-c07a-4d99-aa7a-5f91fcc2823a.jpg"   "img-pa12-wanhua.jpg"

# Иконки применения — страница PA12 Эластомер
download "$BASE/69878007-aca6-4ba9-9680-2fef889a2d67.jpg"   "icon-pa12e-shoe.jpg"
download "$BASE/2a5e1cb6-f909-409a-bf43-e3b2d36fe49f.jpg"   "icon-pa12e-sport.jpg"
download "$BASE/134ccd00-5923-4792-8e16-efc831761e9c.jpg"   "icon-pa12e-pipe.jpg"
# icon-pa12e-belt.jpg, icon-pa12e-film.jpg, icon-pa12e-tough.jpg — нет UUID, используют fallback adv-tech.jpg

# Иконки применения — страница EVOH
download "$BASE/f382dd24-e6d4-466c-942c-9ad755a71b80.jpg"   "icon-evoh-food.jpg"
download "$BASE/127bed8b-e84f-430e-bde0-1b131c2a73c4.jpg"   "icon-evoh-pharma.jpg"
download "$BASE/b8217639-e180-4936-ab7b-b071063d3bbb.jpg"   "icon-evoh-pipe.jpg"
# icon-evoh-tank.jpg, icon-evoh-film.jpg, icon-evoh-bottle.jpg — нет UUID, используют fallback adv-tech.jpg
# Иконки применения — страница EMAA
download "$BASE/50a64eb4-6985-408c-a57a-4ba7ed6c6fad.jpg"   "icon-emaa-golf.jpg"
download "$BASE/14ef4620-b6b6-4efc-9a07-2082650c1eba.jpg"   "icon-emaa-glass.jpg"
download "$BASE/ba5475fb-ae32-4101-a984-82bfc29470af.jpg"   "icon-emaa-perfume.jpg"
# icon-emaa-cosmetics.jpg, icon-emaa-foil.jpg, icon-emaa-ski.jpg — нет UUID, используют fallback adv-tech.jpg
# Иконки применения — страница EAA
download "$BASE/b9044764-e87b-4ff0-bc2c-6b742d8166d6.jpg"   "icon-eaa-packaging.jpg"
download "$BASE/6abf9735-0e83-422f-850c-7d2cf02408d1.jpg"   "icon-eaa-coating.jpg"
download "$BASE/f86e3e58-adf2-4b5e-9da6-1a865d2a3724.jpg"   "icon-eaa-film.jpg"
# icon-eaa-adhesive.jpg, icon-eaa-hotmelt.jpg, icon-eaa-cable.jpg — нет UUID, используют fallback adv-tech.jpg
# Иконки применения — страница EVA
download "$BASE/37ff7c43-4f6e-4db0-963a-617364829e0c.jpg"   "icon-eva-shoe.jpg"
download "$BASE/687db3ee-349d-471a-a11e-f9142f3b0a84.jpg"   "icon-eva-greenhouse.jpg"
download "$BASE/8ba5217a-1748-4d72-af93-c4f835733c89.jpg"   "icon-eva-film.jpg"
download "$BASE/083db749-2731-4e65-adda-3bc0af2c7b7a.jpg"   "icon-eva-cable.jpg"
download "$BASE/7e9777e4-9545-472f-95fa-9abe0332d8f5.jpg"   "icon-eva-solar.jpg"
download "$BASE/1251d7f4-1172-4f2d-b007-179fd8cd0266.jpg"   "icon-eva-hotmelt.jpg"
# Иконки применения — страница OBC
download "$BASE/b1a24f11-d19d-4647-bbcc-fbfa26009bf0.png"   "icon-obc-cable.png"
download "$BASE/6eb3b0ff-9c0a-4e9d-bbbb-1c222870727b.png"   "icon-obc-appliance.png"
download "$BASE/2fb4b112-bcf4-4927-ad0b-1e02af0e6ad1.png"   "icon-obc-shoe.png"
download "$BASE/e602e2c1-0275-468e-8cca-9c3c9f1adf15.png"   "icon-obc-seal.png"
download "$BASE/badfc97a-c005-428e-a1b0-4ffe3af5c2e0.png"   "icon-obc-consumer.png"
download "$BASE/32c65611-73d6-45c1-8ab0-0cec5690a34c.png"   "icon-obc-sport.png"

# Карточки продуктов (страница 1 оригинала)
download "$BASE/4cd71dff-4730-4311-b127-78da665d025c.jpg"   "prod-poe.jpg"
download "$BASE/3ba6fdfa-adb6-422e-b0d6-bca6d0609ec2.jpg"   "prod-pop.jpg"
download "$BASE/8f8c7958-f6ed-436c-aeaf-2b29431507b0.jpg"   "prod-obc.jpg"
download "$BASE/26bbbeb8-471f-4877-b048-025dc5d3f97a.jpg"   "prod-eva.jpg"
download "$BASE/f67821aa-1eae-49b7-999f-2f284cdbb615.jpg"   "prod-eaa.jpg"
download "$BASE/98767a85-e0f7-458e-8260-18be658f63ef.jpg"   "prod-emaa.jpg"
download "$BASE/accf6f68-2032-413d-8e4f-7c45531bafea.jpg"   "prod-evoh.jpg"
download "$BASE/8e7b1afa-7a05-4ac6-a71f-638bc77a66e4.jpg"   "prod-pa12e.jpg"
download "$BASE/4cd71dff-4730-4311-b127-78da665d025c.jpg"   "prod-epdm.jpg"

# ── СТРАНИЦА КОНТАКТОВ (contact.html) ─────────────────────────────
# Герой-баннер контактов
download "$BASE/6f4f5363-f710-4985-99c5-528733449e5f.jpg"   "contact-hero.jpg"
# Фото справа от формы
download "$BASE/e9eaea8c-318f-4e3b-b7ec-578b32f1d0cd.jpg"   "contact-side.jpg"

# ── СТРАНИЦА СКЛАДА (warehouse.html) ──────────────────────────────
# Герой-баннер
download "$BASE/441a7059-2759-45a3-a4f9-98d63f5b5eb6.jpg"   "wh-hero.jpg"

# Галерея — страница 1 (8 фото)
download "$BASE/d2d97b3e-6ab7-49b3-b2a2-601f98e4bcaa.jpg"   "wh-1.jpg"
download "$BASE/4f2b62e3-05b9-4f22-b24b-b98456f6b411.jpg"   "wh-2.jpg"
download "$BASE/7a372b9b-a99e-4708-9f8a-ed58f84d7d7b.jpg"   "wh-3.jpg"
download "$BASE/26e04a04-f1e4-414f-b73a-474f6f2ed631.jpg"   "wh-4.jpg"
download "$BASE/391aad33-f28e-4524-bc6c-32b289bf5e5c.jpg"   "wh-5.jpg"
download "$BASE/4c70a3b0-cfce-45f7-9307-f4cde09ac368.jpg"   "wh-6.jpg"
download "$BASE/0ada6a4b-b7fe-4719-ac74-ca4e24e68f6d.jpg"   "wh-7.jpg"
download "$BASE/f0a8768c-b325-43cd-8ae5-65754a602a2a.jpg"   "wh-8.jpg"
# Галерея — страница 2 (2 фото, UUID загружаются через AJAX — добавить позже)
# download "$BASE/PLACEHOLDER.jpg"   "wh-9.jpg"
# download "$BASE/PLACEHOLDER.jpg"   "wh-10.jpg"

echo ""
echo "📹 Скачивание видео (может занять 1-2 минуты)..."
download "$VIDEO_BASE/c4ee3739-4c52-4ebc-a98c-8c528342d92c.mp4" "company-video.mp4"

echo ""
echo "================================================"
echo "✅ Готово! Файлы сохранены в папку img/"
ls -lh img/
echo ""
echo "Теперь откройте index.html в браузере."
