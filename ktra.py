import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
file_path = 'D:/MP/ktra.csv'
df = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip')
df.columns = df.columns.str.strip()  # Xử lý khoảng trắng trong tên cột

# In danh sách các cột để kiểm tra
print("Các cột trong DataFrame:", df.columns.tolist())

# 1. Xử lý lỗi định dạng ngày (Check-In và Check-Out Date)
df['Check-In Date'] = pd.to_datetime(df['Check-In Date'], errors='coerce', format='%Y-%m-%d')
df['Check-Out Date'] = pd.to_datetime(df['Check-Out Date'], errors='coerce', format='%Y-%m-%d')

# 2. Xử lý giá trị null
df.fillna({
    'Guest Name': 'Unknown', 
    'Check-Out Date': pd.NaT, 
    'Price': 0, 
    'Special Requests': 'No requests'
}, inplace=True)

# 3. Xử lý lỗi định dạng số (Price)
df['Price'] = df['Price'].replace({r'\$': '', 'USD': '', ',': ''}, regex=True)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# 4. Xử lý thông tin trùng lặp
df.drop_duplicates(inplace=True)

# 5. Lỗi chính tả và giá trị không đồng nhất trong cột 'Special Requests'
df['Special Requests'] = df['Special Requests'].str.lower().str.strip()  # Chuyển thành chữ thường và loại bỏ khoảng trắng

# 6. Thêm cột Guest Count và Room Count
if 'Guest Count' not in df.columns:
    df['Guest Count'] = [1] * len(df)  # Tạo cột với giá trị mặc định là 1 nếu không tồn tại

if 'Room Count' not in df.columns:
    df['Room Count'] = [1] * len(df)  # Tạo cột với giá trị mặc định là 1 nếu không tồn tại

# Đảm bảo kiểu dữ liệu đúng
df['Guest Count'] = df['Guest Count'].astype(int)
df['Room Count'] = df['Room Count'].astype(int)

# 7. Xóa thông tin không hợp lệ
df = df.dropna(subset=['Check-In Date', 'Check-Out Date'])  # Xóa các bản ghi có ngày không hợp lệ

# 8. Xóa các bản ghi có Check-In hoặc Check-Out Date không hợp lệ
df = df[(df['Check-In Date'].notnull()) & (df['Check-Out Date'].notnull())]

# 9. Yêu cầu đặc biệt không đồng nhất
df['Special Requests'] = df['Special Requests'].replace({
    r'l(?:ate|early) check[ -]in': 'late check-in', 
    r'check[-]?out': 'check-out'
}, regex=True)

# Lưu dữ liệu đã sửa lỗi vào file mới
output_file_path = 'D:/MP/cleaned_ktra_fixed.csv'
df.to_csv(output_file_path, index=False)
print(f"Dữ liệu đã được sửa lỗi và lưu vào '{output_file_path}'.")

# Vẽ các biểu đồ

# Biểu đồ tròn phân bố theo trạng thái thanh toán
plt.figure(figsize=(6, 6))
#df['Payment Status'] = ['Paid' if i % 3 == 0 else 'Pending' if i % 3 == 1 else 'Unpaid' for i in range(len(df))]  # Cột ví dụ
df['Payment Status'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99'])
plt.title('Phân bố theo trạng thái thanh toán')
plt.ylabel('')  # Loại bỏ tiêu đề trục y
plt.show()

# Doanh thu theo ngày check-in
revenue_per_day = df.groupby(df['Check-In Date'].dt.date)['Price'].sum()

plt.figure(figsize=(10, 6))
revenue_per_day.plot(kind='bar', color='green')
plt.title('Doanh thu theo ngày Check-In')
plt.xlabel('Ngày Check-In')
plt.ylabel('Doanh thu (VND)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Số lượng đặt phòng theo số lượng khách
plt.figure(figsize=(10, 6))
df['Guest Count'].value_counts().sort_index().plot(kind='bar', color='blue')
plt.title('Số lượng đặt phòng theo số lượng khách')
plt.xlabel('Số lượng khách')
plt.ylabel('Số lượng đặt phòng')
plt.tight_layout()
plt.show()

# Số lượng đặt phòng theo số phòng
plt.figure(figsize=(10, 6))
df['Room Count'].value_counts().sort_index().plot(kind='bar', color='purple')
plt.title('Số lượng đặt phòng theo số phòng')
plt.xlabel('Số phòng')
plt.ylabel('Số lượng đặt phòng')
plt.tight_layout()
plt.show()
