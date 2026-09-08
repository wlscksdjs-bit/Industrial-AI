import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from step1_data_eda import MVTecDataset


class StrictBottleneckAE(nn.Module):
    """
    디테일한 결함을 따라 그리지 못하도록 중간 압축률을 극대화한 강력한 병목(Bottleneck) 모델
    """

    def __init__(self):
        super(StrictBottleneckAE, self).__init__()
        # Input: 3 x 256 x 256
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 32, 4, stride=2, padding=1), nn.BatchNorm2d(32), nn.LeakyReLU(0.2),  # 128x128
            nn.Conv2d(32, 64, 4, stride=2, padding=1), nn.BatchNorm2d(64), nn.LeakyReLU(0.2),  # 64x64
            nn.Conv2d(64, 128, 4, stride=2, padding=1), nn.BatchNorm2d(128), nn.LeakyReLU(0.2),  # 32x32
            nn.Conv2d(128, 256, 4, stride=2, padding=1), nn.BatchNorm2d(256), nn.LeakyReLU(0.2),  # 16x16
            # 가장 좁은 병목 구간 (극단적 압축으로 큰 형태만 기억하게 강제함)
            nn.Conv2d(256, 512, 4, stride=2, padding=1), nn.BatchNorm2d(512), nn.LeakyReLU(0.2)  # 8x8
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(512, 256, 4, stride=2, padding=1), nn.BatchNorm2d(256), nn.LeakyReLU(0.2),  # 16x16
            nn.ConvTranspose2d(256, 128, 4, stride=2, padding=1), nn.BatchNorm2d(128), nn.LeakyReLU(0.2),  # 32x32
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1), nn.BatchNorm2d(64), nn.LeakyReLU(0.2),  # 64x64
            nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1), nn.BatchNorm2d(32), nn.LeakyReLU(0.2),  # 128x128
            nn.ConvTranspose2d(32, 3, 4, stride=2, padding=1), nn.Sigmoid()  # 256x256
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))


if __name__ == "__main__":
    ROOT_DIR = './mvtec_ad'
    CATEGORY = 'bottle'
    BATCH_SIZE = 16
    NUM_EPOCHS = 60  # 빠르게 수렴하므로 60에포크면 충분합니다.

    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])

    train_dataset = MVTecDataset(ROOT_DIR, CATEGORY, is_train=True, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"학습 디바이스: {device}")

    model = StrictBottleneckAE().to(device)

    # 꼼수 방지: 가장 정직한 MSE (픽셀 차이) 와 L1 (절대 오차) 만 섞어서 사용
    criterion_mse = nn.MSELoss()
    criterion_l1 = nn.L1Loss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)

    print("강력한 병목 모델 학습 시작...")
    model.train()
    for epoch in range(NUM_EPOCHS):
        epoch_loss = 0
        for images, _, _ in train_loader:
            images = images.to(device)
            outputs = model(images)

            # Loss 계산
            loss = criterion_mse(outputs, images) + 0.5 * criterion_l1(outputs, images)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/{NUM_EPOCHS}], Loss: {epoch_loss / len(train_loader):.4f}')

    SAVE_PATH = 'autoencoder_model_strict.pth'
    torch.save(model.state_dict(), SAVE_PATH)
    print(f"병목 모델 저장 완료: {SAVE_PATH}")