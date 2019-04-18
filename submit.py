from pypai import PAI

pai = PAI('geo', 'geoandPAI,7')
pai.submit(exclude_file=['.mdb', '.jpg', '.png', '.txt', '.pkl', '.pth', '.dat'], exclude_dir=['./.git'])

