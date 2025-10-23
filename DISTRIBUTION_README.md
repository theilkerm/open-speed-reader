# Speed Reader - Dağıtım Dosyaları

Bu klasör Speed Reader uygulamasının dağıtım dosyalarını içerir.

## Dosyalar

### 1. SpeedReader.exe
- **Açıklama**: Uygulamanın tek dosya halindeki çalıştırılabilir versiyonu
- **Boyut**: ~91 MB
- **Kullanım**: Doğrudan çift tıklayarak çalıştırın
- **Gereksinimler**: Windows 10/11 (64-bit)

### 2. SpeedReader_Setup_v1.0.0.exe (Eğer oluşturulduysa)
- **Açıklama**: Profesyonel kurulum dosyası
- **Kullanım**: Çift tıklayarak kurulum sihirbazını başlatın
- **Özellikler**:
  - Otomatik kurulum
  - Masaüstü kısayolu oluşturma
  - Başlat menüsüne ekleme
  - Kaldırma programı

## Kurulum Talimatları

### Yöntem 1: Tek Dosya (Önerilen)
1. `SpeedReader.exe` dosyasını istediğiniz klasöre kopyalayın
2. Dosyaya çift tıklayarak uygulamayı başlatın
3. İlk çalıştırmada Windows Defender uyarısı çıkabilir - "Daha fazla bilgi" > "Yine de çalıştır" seçin

### Yöntem 2: Kurulum Dosyası
1. `SpeedReader_Setup_v1.0.0.exe` dosyasını çalıştırın
2. Kurulum sihirbazını takip edin
3. Kurulum tamamlandıktan sonra uygulamayı başlat menüsünden veya masaüstünden çalıştırın

## Kullanım

1. **Dosya Seçme**: "Select File" butonuna tıklayarak PDF veya EPUB dosyası seçin
2. **Ayarlar**: 
   - Words Per Minute (WPM): Okuma hızını ayarlayın (100-1000)
   - Font Size: Yazı boyutunu ayarlayın (24-200px)
   - Paragraph Pause: Paragraf arası bekleme süresi (0-5 saniye)
   - Theme: Açık/Koyu tema seçin
3. **Okumaya Başlama**: "Start Reading" butonuna tıklayın

## Klavye Kısayolları (Okuma Sırasında)

- **Space**: Oynat/Duraklat
- **S**: Ayarlar
- **Escape**: Ana menüye dön

## Sorun Giderme

### Uygulama Açılmıyor
- Windows Defender'ın uygulamayı engellemediğinden emin olun
- Antivirus yazılımınızın uygulamayı karantinaya almadığını kontrol edin
- Uygulamayı yönetici olarak çalıştırmayı deneyin

### Dosya Açılmıyor
- Desteklenen formatlar: PDF ve EPUB
- Dosyanın bozuk olmadığından emin olun
- Dosya yolunda özel karakterler olmamasına dikkat edin

### Performans Sorunları
- Büyük dosyalar için daha düşük WPM değeri kullanın
- Diğer uygulamaları kapatarak sistem kaynaklarını serbest bırakın

## Teknik Bilgiler

- **Platform**: Windows 10/11 (64-bit)
- **Framework**: PyQt6
- **Desteklenen Formatlar**: PDF (PyMuPDF), EPUB (ebooklib)
- **Dil Desteği**: Türkçe, İngilizce
- **Minimum Sistem Gereksinimleri**:
  - RAM: 4 GB
  - Disk Alanı: 100 MB
  - İşlemci: 1 GHz

## Lisans

Bu uygulama MIT lisansı altında dağıtılmaktadır. Detaylar için LICENSE.md dosyasına bakın.

## Destek

Sorunlarınız için GitHub Issues sayfasını kullanın: https://github.com/yourusername/open-speed-reader/issues
