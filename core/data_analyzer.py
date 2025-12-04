"""
Data Analyzer
Performs statistical analysis and creates visualizations from scraped data
"""

import pandas as pd
import json
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from collections import Counter
import os


class DataAnalyzer:
    """Analyzes scraped data and generates insights"""
    
    def __init__(self, data_file):
        self.data_file = data_file
        self.df = None
        self.analysis_results = {
            'file': data_file,
            'analyzed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'statistics': {},
            'insights': [],
            'charts': []
        }
        
        # Create charts directory
        self.charts_dir = os.path.join(os.path.dirname(data_file), 'charts')
        os.makedirs(self.charts_dir, exist_ok=True)
    
    def load_data(self):
        """Load data from CSV or JSON"""
        print(f"\n📖 Loading data from: {self.data_file}")
        
        try:
            if self.data_file.endswith('.csv'):
                self.df = pd.read_csv(self.data_file, encoding='utf-8-sig')
            elif self.data_file.endswith('.json'):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.df = pd.DataFrame(data)
            else:
                raise ValueError("Unsupported file format. Use CSV or JSON.")
            
            print(f"   ✅ Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
            return True
        
        except Exception as e:
            print(f"   ❌ Error loading data: {e}")
            return False
    
    def basic_statistics(self):
        """Generate basic statistics"""
        print("\n📊 Generating statistics...")
        
        stats = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'columns': list(self.df.columns),
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        }
        
        # Column-specific stats
        column_stats = {}
        
        for col in self.df.columns:
            col_data = {
                'dtype': str(self.df[col].dtype),
                'non_null': int(self.df[col].count()),
                'null': int(self.df[col].isnull().sum()),
                'unique': int(self.df[col].nunique())
            }
            
            # For numeric columns
            if pd.api.types.is_numeric_dtype(self.df[col]):
                col_data['mean'] = float(self.df[col].mean()) if not self.df[col].isnull().all() else None
                col_data['median'] = float(self.df[col].median()) if not self.df[col].isnull().all() else None
                col_data['std'] = float(self.df[col].std()) if not self.df[col].isnull().all() else None
                col_data['min'] = float(self.df[col].min()) if not self.df[col].isnull().all() else None
                col_data['max'] = float(self.df[col].max()) if not self.df[col].isnull().all() else None
            
            # For text columns
            elif pd.api.types.is_string_dtype(self.df[col]):
                # Calculate average text length
                text_lengths = self.df[col].dropna().astype(str).str.len()
                if len(text_lengths) > 0:
                    col_data['avg_length'] = float(text_lengths.mean())
                    col_data['max_length'] = int(text_lengths.max())
                    col_data['min_length'] = int(text_lengths.min())
            
            column_stats[col] = col_data
        
        stats['column_details'] = column_stats
        
        self.analysis_results['statistics'] = stats
        
        print(f"   ✅ Statistics generated for {len(self.df.columns)} columns")
    
    def generate_insights(self):
        """Generate human-readable insights"""
        print("\n🔍 Generating insights...")
        
        insights = []
        
        # Dataset size insight
        insights.append({
            'type': 'size',
            'message': f"Dataset contains {len(self.df)} records across {len(self.df.columns)} columns."
        })
        
        # Column insights
        for col in self.df.columns:
            # Check for missing data
            null_pct = (self.df[col].isnull().sum() / len(self.df)) * 100
            if null_pct > 50:
                insights.append({
                    'type': 'warning',
                    'column': col,
                    'message': f"Column '{col}' has {null_pct:.1f}% missing data."
                })
            
            # Check for duplicate values
            if self.df[col].nunique() == len(self.df) and len(self.df) > 1:
                insights.append({
                    'type': 'info',
                    'column': col,
                    'message': f"Column '{col}' contains unique values (potential ID field)."
                })
            
            # Check for text columns
            if pd.api.types.is_string_dtype(self.df[col]):
                non_null = self.df[col].dropna()
                if len(non_null) > 0:
                    avg_len = non_null.astype(str).str.len().mean()
                    if avg_len > 200:
                        insights.append({
                            'type': 'info',
                            'column': col,
                            'message': f"Column '{col}' contains long text (avg {avg_len:.0f} characters)."
                        })
        
        # Most common values in categorical columns
        for col in self.df.columns:
            if self.df[col].nunique() < 20 and self.df[col].nunique() > 1:
                top_value = self.df[col].value_counts().index[0]
                top_count = self.df[col].value_counts().iloc[0]
                insights.append({
                    'type': 'distribution',
                    'column': col,
                    'message': f"Most common value in '{col}': '{top_value}' ({top_count} occurrences)"
                })
        
        self.analysis_results['insights'] = insights
        
        print(f"   ✅ Generated {len(insights)} insights")
    
    def create_visualizations(self):
        """Create charts and visualizations"""
        print("\n📊 Creating visualizations...")
        
        charts_created = []
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
        
        # 1. Data completeness chart
        chart_path = self._create_completeness_chart()
        if chart_path:
            charts_created.append(chart_path)
        
        # 2. Column distribution charts (for categorical data)
        for col in self.df.columns:
            if self.df[col].nunique() < 20 and self.df[col].nunique() > 1:
                chart_path = self._create_distribution_chart(col)
                if chart_path:
                    charts_created.append(chart_path)
                
                if len(charts_created) >= 5:  # Limit number of charts
                    break
        
        # 3. Numeric distributions
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols[:3]:  # First 3 numeric columns
            chart_path = self._create_histogram(col)
            if chart_path:
                charts_created.append(chart_path)
        
        self.analysis_results['charts'] = charts_created
        
        print(f"   ✅ Created {len(charts_created)} visualizations")
        
        return charts_created
    
    def _create_completeness_chart(self):
        """Create data completeness bar chart"""
        try:
            null_counts = self.df.isnull().sum()
            complete_counts = len(self.df) - null_counts
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            x = range(len(self.df.columns))
            width = 0.35
            
            ax.bar([i - width/2 for i in x], complete_counts, width, label='Complete', color='#2ecc71')
            ax.bar([i + width/2 for i in x], null_counts, width, label='Missing', color='#e74c3c')
            
            ax.set_xlabel('Columns')
            ax.set_ylabel('Count')
            ax.set_title('Data Completeness by Column')
            ax.set_xticks(x)
            ax.set_xticklabels(self.df.columns, rotation=45, ha='right')
            ax.legend()
            
            plt.tight_layout()
            
            chart_path = os.path.join(self.charts_dir, 'data_completeness.png')
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return chart_path
        
        except Exception as e:
            print(f"   ⚠️  Could not create completeness chart: {e}")
            return None
    
    def _create_distribution_chart(self, column):
        """Create distribution chart for categorical column"""
        try:
            value_counts = self.df[column].value_counts().head(10)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            bars = ax.barh(range(len(value_counts)), value_counts.values, color='#3498db')
            ax.set_yticks(range(len(value_counts)))
            ax.set_yticklabels([str(v)[:30] for v in value_counts.index])
            ax.set_xlabel('Count')
            ax.set_title(f'Top 10 Values in "{column}"')
            ax.invert_yaxis()
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2, 
                       f' {int(width)}', ha='left', va='center')
            
            plt.tight_layout()
            
            safe_col_name = "".join(c if c.isalnum() else "_" for c in column)
            chart_path = os.path.join(self.charts_dir, f'distribution_{safe_col_name}.png')
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return chart_path
        
        except Exception as e:
            print(f"   ⚠️  Could not create distribution chart for {column}: {e}")
            return None
    
    def _create_histogram(self, column):
        """Create histogram for numeric column"""
        try:
            data = self.df[column].dropna()
            
            if len(data) == 0:
                return None
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            ax.hist(data, bins=30, color='#9b59b6', edgecolor='black', alpha=0.7)
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')
            ax.set_title(f'Distribution of "{column}"')
            ax.grid(axis='y', alpha=0.3)
            
            # Add statistics
            stats_text = f'Mean: {data.mean():.2f}\nMedian: {data.median():.2f}\nStd: {data.std():.2f}'
            ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
                   verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            plt.tight_layout()
            
            safe_col_name = "".join(c if c.isalnum() else "_" for c in column)
            chart_path = os.path.join(self.charts_dir, f'histogram_{safe_col_name}.png')
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return chart_path
        
        except Exception as e:
            print(f"   ⚠️  Could not create histogram for {column}: {e}")
            return None
    
    def save_analysis(self, output_path):
        """Save analysis results to JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Analysis saved to: {output_path}")
    
    def print_summary(self):
        """Print analysis summary"""
        print("\n" + "=" * 100)
        print("📊 DATA ANALYSIS SUMMARY")
        print("=" * 100)
        
        stats = self.analysis_results['statistics']
        print(f"\n📋 Dataset:")
        print(f"   Rows: {stats['total_rows']}")
        print(f"   Columns: {stats['total_columns']}")
        print(f"   Memory: {stats['memory_usage']}")
        
        print(f"\n🔍 Key Insights:")
        for insight in self.analysis_results['insights'][:5]:
            print(f"   • {insight['message']}")
        
        print(f"\n📊 Visualizations:")
        print(f"   Created {len(self.analysis_results['charts'])} charts")
        
        print("\n" + "=" * 100)
    
    def run_full_analysis(self, output_path=None):
        """Run complete analysis"""
        if not self.load_data():
            return None
        
        self.basic_statistics()
        self.generate_insights()
        self.create_visualizations()
        
        if output_path:
            self.save_analysis(output_path)
        
        self.print_summary()
        
        return self.analysis_results


def analyze_data(data_file, output_file=None):
    """Convenience function"""
    analyzer = DataAnalyzer(data_file)
    return analyzer.run_full_analysis(output_file)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        analyze_data(data_file, output_file)
    else:
        print("Usage: python data_analyzer.py <data.csv|data.json> [analysis.json]")
