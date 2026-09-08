import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, precision_recall_curve
from torchvision import transforms
from torch.utils.data import DataLoader
from step1_data_eda import MVTecDataset

# =========================================================================
# [핵심] 1단계에서 학습한 파일('step2_train_strict.py')에서 모델 구조를 가져옵니다.
# =========================================================================
from step2_train import StrictBottleneckAE


def evaluate_performance(model, test_loader, device, blur_kernel=(21, 21), top_k_ratio=0.01):
    model.eval()
    y_true = []
    y_scores = []

    print("전체 테스트 데이터셋 정량 평가를 진행합니다...")
    with torch.no_grad():
        for images, labels, _ in test_loader:
            images = images.to(device)
            outputs = model(images)

            # 오차 계산 및 블러 처리
            error = torch.mean((images - outputs) ** 2, dim=1)
            error_map = error.squeeze().cpu().numpy()
            error_map = cv2.GaussianBlur(error_map, blur_kernel, 0)

            # Anomaly Score 산출
            flat_error = error_map.flatten()
            num_pixels = max(1, int(len(flat_error) * top_k_ratio))
            flat_error.sort()
            anomaly_score = np.mean(flat_error[-num_pixels:])

            y_scores.append(anomaly_score)
            y_true.append(labels.item())

            # 정량적 지표 계산
    auroc = roc_auc_score(y_true, y_scores)
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_scores)

    f1_scores = (2 * precisions * recalls) / (precisions + recalls + 1e-8)
    best_idx = np.argmax(f1_scores)
    best_f1 = f1_scores[best_idx]
    best_threshold = thresholds[best_idx]

    print("-" * 40)
    print(f"[강력한 병목 모델 최종 평가 결과]")
    print(f"AUROC Score          : {auroc:.4f}")
    print(f"Best F1-Score        : {best_f1:.4f}")
    print(f"Optimal Threshold    : {best_threshold:.4f}")
    print("-" * 40)

    return best_threshold


def visualize_anomaly(model, test_loader, device, threshold, blur_kernel=(21, 21), top_k_ratio=0.01, num_samples=3):
    model.eval()
    samples_shown = 0

    print(f"\n최적 임계값({threshold:.4f})을 적용하여 시각화를 시작합니다.")

    with torch.no_grad():
        for images, labels, _ in test_loader:
            if labels.item() == 0:
                continue

            images = images.to(device)
            outputs = model(images)

            error = torch.mean((images - outputs) ** 2, dim=1)
            error_map = error.squeeze().cpu().numpy()
            error_map = cv2.GaussianBlur(error_map, blur_kernel, 0)

            flat_error = error_map.flatten()
            num_pixels = max(1, int(len(flat_error) * top_k_ratio))
            flat_error.sort()
            anomaly_score = np.mean(flat_error[-num_pixels:])
            prediction = "NG (Defect)" if anomaly_score >= threshold else "OK (Normal)"

            error_map_norm = cv2.normalize(error_map, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            heatmap = cv2.applyColorMap(error_map_norm, cv2.COLORMAP_JET)

            img_np = images.squeeze().cpu().permute(1, 2, 0).numpy()
            out_np = outputs.squeeze().cpu().permute(1, 2, 0).numpy()
            heatmap_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
            overlay = cv2.addWeighted((img_np * 255).astype(np.uint8), 0.5, heatmap_rgb, 0.5, 0)

            fig, axes = plt.subplots(1, 4, figsize=(16, 4))
            axes[0].imshow(img_np);
            axes[0].set_title(f'Original\nScore: {anomaly_score:.4f} -> {prediction}')
            axes[1].imshow(out_np);
            axes[1].set_title('Reconstructed')
            axes[2].imshow(error_map, cmap='hot');
            axes[2].set_title('Error Map')
            axes[3].imshow(overlay);
            axes[3].set_title('Overlay Heatmap')

            for ax in axes:
                ax.axis('off')
            plt.show()

            samples_shown += 1
            if samples_shown >= num_samples:
                break


if __name__ == "__main__":
    ROOT_DIR = './mvtec_ad'
    CATEGORY = 'bottle'

    # 💡 1단계에서 새로 저장된 가중치 파일명을 바라봅니다.
    MODEL_PATH = 'autoencoder_model_strict.pth'

    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])

    test_dataset = MVTecDataset(ROOT_DIR, CATEGORY, is_train=False, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 💡 1단계에서 학습한 모델(StrictBottleneckAE)을 생성하고 가중치를 입힙니다.
    model = StrictBottleneckAE().to(device)
    model.load_state_dict(torch.load(MODEL_PATH))

    OPTIMAL_BLUR_KERNEL = (21, 21)
    OPTIMAL_TOP_K_RATIO = 0.01

    optimal_thresh = evaluate_performance(
        model, test_loader, device,
        blur_kernel=OPTIMAL_BLUR_KERNEL,
        top_k_ratio=OPTIMAL_TOP_K_RATIO
    )

    visualize_anomaly(
        model, test_loader, device, optimal_thresh,
        blur_kernel=OPTIMAL_BLUR_KERNEL,
        top_k_ratio=OPTIMAL_TOP_K_RATIO,
        num_samples=3
    )